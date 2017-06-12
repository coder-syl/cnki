# coding=utf8
from flask import render_template, request
from . import bp
from app.models import *
from app import q, db
import requests
import time
from rq import Queue
from app.helper import crawler
from math import ceil
from sqlalchemy.sql import text
import more_itertools

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

@bp.route('/', methods=['GET', 'POST'])
def index():
    papers_count = db.session.query(Paper).count()
    keywords_count = db.session.query(Keyword).count()
    return render_template('main/index.html',
                           papers_count=papers_count,
                           keywords_count=keywords_count)

@bp.route('/search_query', methods=['GET'])
def search_query():
    query = request.args.get('query')
    query_results = db.session.query(Paper).filter(Paper.title.like("%{0}%".format(query))).all()
    result_sql = text("select keyword_id, count(*) FROM keywords where paper_id in :paper_ids GROUP BY keyword_id ORDER BY count(*) DESC limit 10;")
    result = db.engine.execute(result_sql, paper_ids=tuple([k.id for k in query_results])).fetchall()
    top10_keywords = [{'keyword': db.session.query(Keyword).get(r[0]).keyword, 'count': r[1]} for r in result]
    keywords_label = [k['keyword'] for k in top10_keywords]
    counts = [k['count'] for k in top10_keywords]
    year_result_sql = text(
            "select year, count(*) from paper where title like :query group by year order by count(*);"
    )
    years_result = [tuple([k, v]) for k,v in db.engine.execute(year_result_sql, query='%{0}%'.format(query)).fetchall() if k]
    years_label = [r[0] for r in years_result]
    years_counts = [r[1] for r in years_result]

    orgs_result = [(db.session.query(Organization).get(a).organization, b) for a,b in [(k, v) for k, v in db.engine.execute("select orgainzation_id, count(*) from organizations where paper_id in {0} group by orgainzation_id order by count(*) desc limit 10;".format(tuple([p.id for p in query_results])))]]
    orgs_label = [r[0] for r in orgs_result]
    orgs_counts = [r[1] for r in orgs_result]

    return render_template('main/more.html', top10_keywords=top10_keywords,
                           keywords_label=keywords_label, counts=counts,
                           years_label=years_label, years_counts=years_counts,
                           years_result=years_result, orgs_label=orgs_label,
                           orgs_counts=orgs_counts)



@bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    page = request.args.get('page', type=int, default=1)
    per_page = 10
    papers = db.session.query(Paper).filter(Paper.title.like("%{0}%"\
            .format(query))).offset((page-1)*per_page).limit(per_page)
    total_pages = int(ceil(db.session.query(Paper).count() / per_page))
    count = db.session.query(Paper).filter(Paper.title.like("%{0}%".format(query))).count()
    return render_template('main/papers.html', papers=papers, page=page, total_pages=total_pages, query=query)

@bp.route('/paper/<int:id>')
def paper(id):
    paper = db.session.query(Paper).get(id)
    return render_template('main/paper.html', paper=paper)

@bp.route('/author/<int:id>')
def author(id):
    author = db.session.query(Author).get(id)
    author_papers = author.papers
    related_authors = []
    related_authors_meta = []
    for p in author_papers:
        for a in p.authors:
            #if not a == author and a not in related_authors_meta:
            if not a == author:
                is_in = False
                for i in related_authors:
                    if a.id == i['id']:
                        is_in = True

                if not is_in:
                    related_authors.append({'id': a.id, 'author': a.author, 'times': 1})
                if a in related_authors_meta:
                    for i, dic in enumerate(related_authors):
                        if dic['id'] == a.id:
                            dic['times'] += 1
                related_authors_meta.append(a)
    print(related_authors)

    papers_join_sql = text("select paper_id from author inner join authors on author.id = authors.author_id where author.id=:author_id;")
    papers_join = [r[0] for r in db.engine.execute(papers_join_sql, author_id=id).fetchall()]
    papers = db.session.query(Paper).filter(Paper.id.in_(tuple(papers_join))).all()
    keywords = []
    keywords_meta = []
    for paper in author.papers:
        for keyword in paper.keywords:
            is_in = False
            for i in keywords:
                if keyword.id == i['id']:
                    is_in = True
            if not is_in:
                keywords.append({'id': keyword.id, 'keyword': keyword.keyword, 'times': 1})
            if keyword in keywords_meta:
                for i, dic in enumerate(keywords):
                    if dic['id'] == keyword.id:
                        dic['times'] += 1
            keywords_meta.append(keyword)

    return render_template('main/author.html', author=author, papers=papers,
                           related_authors=related_authors, keywords=keywords)

@bp.route('/more', methods=['GET'])
def more():
    result = db.engine.execute("select keyword_id, count(*) FROM keywords GROUP BY keyword_id ORDER BY count(*) DESC;").fetchall()
    # top 10 keywords
    top10_keywords = [{'keyword': db.session.query(Keyword).get(r[0]).keyword, 'count': r[1]} for r in result[0:10]]
    keywords_label = [k['keyword'] for k in top10_keywords]
    counts = [k['count'] for k in top10_keywords]
    years_result = [tuple([k, v]) for k,v in db.engine.execute("select year, count(*) from paper group by year order by count(*);").fetchall() if k]
    orgs_result = [(db.session.query(Organization).get(a).organization, b) for a,b in [(k, v) for k, v in db.engine.execute("select orgainzation_id, count(*) from organizations group by orgainzation_id order by count(*) desc limit 10;")]]
    orgs_label = [r[0] for r in orgs_result]
    orgs_counts = [r[1] for r in orgs_result]
    #years_result = db.engine.execute("select year, count(*) from paper group by year order by count(*) desc;").fetchall()
    years_label = [r[0] for r in years_result]
    years_counts = [r[1] for r in years_result]
    return render_template('main/more.html', top10_keywords=top10_keywords,
                           keywords_label=keywords_label,
                           counts=counts, years_result=years_result,
                           years_label=years_label, years_counts=years_counts,
                           orgs_label=orgs_label, orgs_counts=orgs_counts)

@bp.route('/consume', methods=['GET'])
def consume():
    while True:
        papers = db.session.query(Paper).filter((Paper.in_queue == None)\
                | (Paper.in_queue == 0)).all()

        # push paper to queue
        #for paper in papers[1:10]:
        for paper in papers:
            job = q.enqueue(crawler, paper.id, paper.url)
            time.sleep(3)
            result = job.result
            if result:
                print(result)
                keywords = result['keywords']
                organizations = result['organizations']
                authors = result['authors']
                record_keywords = []
                record_organizations = []
                record_authors = []
                if keywords:
                    for keyword in keywords:
                        keyword = get_or_create(db.session, Keyword, keyword=keyword)
                        record_keywords.append(keyword)
                        db.session.add(keyword)
                else:
                    record_keywords = []

                for organization in organizations:
                    organization = get_or_create(db.session, Organization, organization=organization)
                    record_organizations.append(organization)
                    db.session.add(organization)

                for author in authors:
                    author = get_or_create(db.session, Author, author=author)
                    record_authors.append(author)
                    db.session.add(author)

                paper.description = result['abstract']
                paper.year = result['year']
                paper.in_queue = 1
                paper.keywords = record_keywords
                paper.organizations = record_organizations
                paper.authors = record_authors
                db.session.add(paper)
                db.session.commit()
