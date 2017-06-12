from . import db

keywords = db.Table('keywords',
    db.Column('paper_id', db.Integer, db.ForeignKey('paper.id')),
    db.Column('keyword_id', db.Integer, db.ForeignKey('keyword.id'))
)

organizations = db.Table('organizations',
    db.Column('paper_id', db.Integer, db.ForeignKey('paper.id')),
    db.Column('orgainzation_id', db.Integer, db.ForeignKey('organization.id'))
)

authors = db.Table('authors',
    db.Column('paper_id', db.Integer, db.ForeignKey('paper.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    url = db.Column(db.String(300))
    source = db.Column(db.String(50))
    description = db.Column(db.Text)
    #authors = db.Column(db.String(500))
    in_queue = db.Column(db.Integer, default=0)
    query = db.Column(db.String(10))
    keywords = db.relationship('Keyword', secondary=keywords,
            backref=db.backref('papers', lazy='dynamic'))
    organizations = db.relationship('Organization', secondary=organizations,
            backref=db.backref('organizations', lazy='dynamic'))
    authors = db.relationship('Author', secondary=authors,
            backref=db.backref('authors', lazy='dynamic'))
    year = db.Column(db.String(10))
    __table_args__ = (db.UniqueConstraint('url', 'query', name='url_query_uc'), )

    def __init__(self):
        self.in_queue = 0

class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.Text)
    url = db.Column(db.Text)

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.Text)
    url = db.Column(db.Text)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(20))
    url = db.Column(db.Text)
    papers = db.relationship('Paper', secondary=authors,
            backref=db.backref('papers', lazy='dynamic'))
