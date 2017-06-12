from bs4 import BeautifulSoup
with open('page.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'lxml')
results = soup.select('.GridTableContent tr')
for r in results:
    if r.has_attr('bgcolor'):
        hh = r.select('td')[1].find('a')
        print(hh)
        print('--')
