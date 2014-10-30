#!/usr/bin/python -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

"""A tiny Python program to check that Python is working.
Try running this program from the command line like this:
  python hello.py
  python hello.py Alice
That should print:
  Hello World -or- Hello Alice
Try changing the 'Hello' to 'Howdy' and run again.
Once you have that working, you're ready for class -- you can edit
and run Python code; now you just need to learn Python!
"""

import sys
import requests
import codecs
import re
from lxml import html

#
# Define a main() function that prints a little greeting.
def main():
  # Get the name from the command line, using 'World' as a fallback.
  if len(sys.argv) >= 2:
    name = sys.argv[1]
  else:
    name = 'World'
  print 'Hello', name
#  sys.setdefaultencoding('utf-8')
  f = codecs.open('a.html', 'r', 'utf-8')
#  print f.read()
  tree = html.fromstring(f.read())
  tab_select = '//div[@class="facet-result cmpr_listing"]'
  li = tree.xpath(tab_select)
  print tab_select
  j = 0
  for items in li:
    j += 1
    model = items[1].find('div/h1/a').text_content().strip()
    if 'T440s' not in model:
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
#  print 
#  print li
#  li = tree.xpath(tab_select)
#  for items in li:
#    if items[UID].text_content().strip() == user:
#      print 'gid: ' + items[GID].text_content().strip()+ ' status: ' + items[STATUS].text_content().strip()
#      print 'title: ' + items[SUBJECT].text_content().strip()
#      print '------------------'
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

