# coding=utf8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import sys
import MySQLdb


db = MySQLdb.connect(host="localhost", user="root", password="52shangxian", db="cnki",  use_unicode=True, charset="utf8")
c = db.cursor()

url = "http://kns.cnki.net/kns/brief/default_result.aspx"
browser = webdriver.Firefox()
browser.get(url)
search_box = browser.find_element_by_css_selector('.research .rekeyword')
arg = sys.argv[1:][0]

search_box.send_keys(str(arg) + Keys.RETURN)
try:
    #time.sleep(10)
    frame = browser.find_element_by_xpath("//*[@id='iframeResult']")
    browser.switch_to.frame(frame)
    eles = browser.find_elements_by_css_selector('.GridTableContent tbody tr td:nth-child(2) a')
    data = [{'url': ele.get_attribute('href'), 'title': ele.text} for ele in eles]
    c.executemany(
        """insert ignore into paper (title, url) values (%s, %s)""",
        [(d['title'], d['url']) for d in data])
    db.commit()

except Exception as e:
    print(e)

browser.quit()
