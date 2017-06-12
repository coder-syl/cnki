import requests
import MySQLdb
import time
import sys
try:
    from http.cookiejar import MozillaCookieJar
except ImportError:
    from cookielib import MozillaCookieJar
from bs4 import BeautifulSoup

db = MySQLdb.connect(host="localhost", user="root", password="52shangxian", db="cnki",  use_unicode=True, charset="utf8")
c = db.cursor()
query = sys.argv[1:][0]

cookies = {
    'ASP.NET_SessionId': '2i3bqc5yrvmznfrrt3v5sqwk',
    'cnkiUserKey': '073365b7-5b91-06e1-7f7b-b89cd7cfaf77',
    'Ecp_ClientId': '2170407235904575751',
    'Ecp_IpLoginFail': '170523124.66.49.63',
    'RsPerPage': '50',
    'SID_crrs': '125132',
    'SID_klogin': '125142',
    'SID_kns': '123107',
    'SID_kredis': '125144',
    'SID_krsnew': '125134',
    'UM_distinctid': '15bd8825fa184-07ca3fa9b37f77-153a655c-fa000-15bd8825fa2c75'
}

cookies = dict(cookies)
urls = ['http://kns.cnki.net/kns/brief/brief.aspx?curpage={0}&RecordsPerPage=50&QueryID=0&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_default_result_aspx#J_ORDER&'.format(page) for page in range(1, 120)]
for url in urls:
    #time.sleep(10)
    r = requests.get(url, cookies=cookies)
    #with open('xx.html', 'wb') as f:
    #f.write(r.content)
    soup = BeautifulSoup(r.text, 'lxml')
    results = soup.select('.GridTableContent tr')

    print('requesting ' + url)
    if not results:
        print('请到 ' + url + ' 输入验证码, 输入完毕且正确后请打y')
        is_success = input()
        if is_success == 'y':
            continue
        else:
            print('请重新输入验证码')
    else:
        for r in results:
            if r.has_attr('bgcolor'):
                record = r.select('td')[1].find('a')
                year = r.select('td')[4].text
                url = 'http://kns.cnki.net' + record.attrs['href']
                title = record.text
                c.execute(
                    """insert ignore into paper (title, url, query, year) values (%s, %s, %s, %s)""",
                    (title ,url, query, year))
                db.commit()
