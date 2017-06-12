from bs4 import BeautifulSoup

with open('output4.html', 'rb') as f:
    html = f.read()
    soup = BeautifulSoup(html, 'lxml')
    links = soup.select(".sourinfo a")
    print(links[2].text.strip()[0:4])
