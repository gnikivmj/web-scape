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

it = 6
sleep_time = 300
#url = "http://outlet.lenovo.com/outlet_us/laptops/#/?page-index=1&page-size=100&facet-1=3&sort-criteria=2"
url = "http://outlet.lenovo.com/outlet_us/laptops/#/?page-index=1&page-size=100&facet-1=1&facet-1=3&facet-3=14&facet-3=19&facet-5=4&sort-criteria=2"

model_to_look = [{'model':'T440s', 'price':800}, {'model':'Carbon', 'price':920}]

def fetch_content():
  display = Display(visible=0, size=(800, 600))
  display.start()

  driver = webdriver.Firefox()
  driver.get(url)
  driver.set_window_size(1000,1000)
  for i in range(0, it):
    time.sleep(4)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

  content = driver.page_source
  driver.close()
  driver.quit()
  display.stop()
  return content

def parse_content(content):
  tree = html.fromstring(content)
  tab_select = '//div[@class="facet-result cmpr_listing"]'
  li = tree.xpath(tab_select)
  print tab_select

  for items in li:
    prices = items[2].find('div[@class="pricing"]/dl/dd[@class="aftercoupon value"]')#/dl/dd[@class="ftercoupon value"]')
    p = re.sub('[$,]', '', prices.text_content().strip())

    model = items[1].find('div/h1/a').text_content().strip()

    find = False
    for m in model_to_look:
      if m['model'] in model and float(p) < m['price']:
        find = True

    if find == False:
      continue

    print model

    # find the detail information
    part = items[1].find('div[@class="fbr-partnum"]').text_content().strip()
    print 'http://outlet.lenovo.com/outlet_us/itemdetails/' + re.search(r'Part number: (.+)', part).group(1) + '/445'
    print part
    features = items[1].find('ul[@class="fbr-features"]')
    for feature in features[1:]:
      print " ".join(feature.text_content().strip().encode('ascii','ignore').split())

    # find the price information
    count = items[2].find('div/span')
    if count is not None:
      print 'Count:', count.text_content().strip()
    prices = items[2].find('div[@class="pricing"]/dl/dd[@class="aftercoupon value"]')#/dl/dd[@class="ftercoupon value"]')
    print prices.text_content().strip()
    print '-----'

  print 'total count ', len(li)
  print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

  return

if __name__ == "__main__":
  if len(sys.argv) >= 2:
     option  = sys.argv[1]
  else:
     option = None

  if option == '--local':
    f = codecs.open('sample.html', 'r', 'utf-8')
    content = f.read()
    parse_content(content)
  elif option == '--save':
    content = fetch_content()
    f = codecs.open('sample.html', 'w', 'utf-8')
    f.write(content)
    f.close()
  else:
    while True:
      print "fetch content ...", time.ctime()
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
