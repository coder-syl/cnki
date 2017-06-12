# coding=utf8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def crawler(id, url):
    url = get_real_url(url)
    resp = requests.get(url)
    print('requesting ' + url)
    soup = BeautifulSoup(resp.text, "lxml")
    abstract = soup.select('span#ChDivSummary')[0].text
    keyword_label = soup.find(id='catalog_KEYWORD')
    try:
        keywords = [key.text.strip().replace(';', '').replace('\n', '').replace('\r', '') for key in keyword_label.find_next_siblings("a")]
    except:
        keywords = None
    try:
        year = soup.select(".sourinfo a")[2].text.strip()[0:4]
    except:
        year = None
    orgs = [s.text for s in soup.select(".orgn a")]
    authors = [s.text for s in soup.select('.author a')]
    result = {'abstract': abstract, 'keywords': keywords, 'year': year, 'organizations': orgs, 'authors': authors}
    print(result)
    return result

def get_real_url(url):
    parsed_url = urlparse(url)
    parsed_qs = parse_qs(parsed_url.query)
    dbcode = parsed_qs['DbCode'][0]
    dbname = parsed_qs['DbName'][0]
    filename = parsed_qs['FileName'][0]
    real_url = 'http://kns.cnki.net/KCMS/detail/detail.aspx?dbcode={0}&dbname={1}&filename={2}'.format(dbcode, dbname, filename)
    return real_url
