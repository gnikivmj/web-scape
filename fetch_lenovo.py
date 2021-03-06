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

it = 25
sleep_time = 300
url ="http://outlet.lenovo.com/outlet_us/laptops/#facet-1=1,2,3&facet-2=1&facet-3=14"

model_to_look = [{'model':'T440s', 'price':800}, {'model':'Carbon', 'price':940}]

def fetch_content():
  display = Display(visible=0, size=(800, 600))
  display.start()

  try:
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(15)
    driver.get(url)
    driver.set_window_size(1000,1000)
    for i in range(0, it):
      time.sleep(4)
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    content = driver.page_source
    driver.close()
    driver.quit()
    display.stop()
  except:
    print "exception !!!"
    driver.close()
    driver.quit()
    display.stop()
    content = None
  return content

def parse_content(content):
  tree = html.fromstring(content)
  tab_select = '//div[@class="facetedResults-item only-allow-small-pricingSummary"]'
  li = tree.xpath(tab_select)
  print tab_select

  print 'looking for:'
  for m in model_to_look:
    print m['model'] + ' < $' + str(m['price'])

  for items in li:
    prices = items[2].find('div/div/dl/dd[@class="aftercoupon pricingSummary-details-final-price"]')
    p = re.sub('[$,]', '', prices.text_content().strip())
    model = items[1].find('h3/a').text_content().strip()

    find = False
    for m in model_to_look:
      if m['model'] in model and float(p) < m['price']:
        find = True

    if find != True:
      continue

    print model

    # find the detail information
    part = items[1].find('div').text_content().strip()
    print 'http://outlet.lenovo.com/outlet_us/itemdetails/' + re.search(r'Part number: (.+)', part).group(1) + '/445'
    print part

    features = items[2].find('div/div[@class="facetedResults-feature-list"]')
    for feature in features[1:]:
      print " ".join(feature.text_content().strip().encode('ascii','ignore').split())

    # find the price information
    count = items[2].find('div/div/div')#/div[@class="instock heart"]')
    #print count.text_content()
    if count is not None:
      print 'Count:', count.text_content().strip()
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
      if content is not None:
        print "parsing ...", time.ctime()
        parse_content(content)
      print time.ctime(), "sleep for %ss" % sleep_time
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
