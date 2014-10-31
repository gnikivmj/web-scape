#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from lxml import html

import sys
import codecs
import time
import requests
import re

it = 18
sleep_time = 300
url = "http://outlet.lenovo.com/outlet_us/laptops/#/?page-index=1&page-size=100&facet-1=3&sort-criteria=2"

def fetch_content():
  display = Display(visible=0, size=(800, 600))
  display.start()

  driver = webdriver.Firefox()
  driver.get(url)
  driver.set_window_size(1000,1000)
  for i in range(0, it):
    time.sleep(4)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#  f = codecs.open("a.html", "w", "utf-8")
#  f.write(driver.page_source)
#  f.close()
  content = driver.page_source
  driver.close()
  display.stop()
  return content

def parse_content(content):
  tree = html.fromstring(content)
  tab_select = '//div[@class="facet-result cmpr_listing"]'
  li = tree.xpath(tab_select)
  print tab_select
  j = 0
  for items in li:
    j += 1
    model = items[1].find('div/h1/a').text_content().strip()
    if 'T440s' not in model and 'Carbon' not in model:
      continue

    prices = items[2].find('div[@class="pricing"]/dl/dd[@class="aftercoupon value"]')#/dl/dd[@class="ftercoupon value"]')
    p = re.sub('[$,]', '', prices.text_content().strip())
    if float(p) > 900:
      continue

    print model
    print items[1].find('div[@class="fbr-partnum"]').text_content().strip()
    features = items[1].find('ul[@class="fbr-features"]')
    for feature in features[1:]:
      print " ".join(feature.text_content().strip().encode('ascii','ignore').split())
    prices = items[2].find('div[@class="pricing"]/dl/dd[@class="aftercoupon value"]')#/dl/dd[@class="ftercoupon value"]')
    print prices.text_content().strip()
    print '-----'
  print 'total count ', j
  print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
#
  return 0

if __name__ == "__main__":
   while True:
    print "fetch content ..."
    content = fetch_content()
    print "parsing ...", time.ctime()
    parse_content(content)
    print time.ctime(), "sleep for %s" % sleep_time
    time.sleep(sleep_time)
"""
display = Display(visible=0, size=(800, 600))
display.start()

driver = webdriver.Firefox()
driver.get(url)
driver.set_window_size(1000,1000)
i = 0
for i in range(0,18):
#  i += 1
  time.sleep(4)
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

f = codecs.open("a.html", "w", "utf-8")
f.write(driver.page_source)
f.close()
driver.close()
display.stop()
"""
