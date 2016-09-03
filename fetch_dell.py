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
import urllib2
import sys
import requests
import codecs
import re
import time
from lxml import html

sleep_time = 300

#
# Define a main() function that prints a little greeting.
def parse_content(content):
  tree = html.fromstring(content)
  tab_select = '//table[@class="fl-width100 fl-topline"]'
  li = tree.xpath(tab_select)
  #print tab_select
  #print li
  j = 0
  for items in li:
    j += 1
    title = items.find_class('fl-inv-head')[0].text_content().strip()
    if '7310' in title:
      print title
      print items.find_class('fl-inv-price')[0].text_content().strip()
      print "++++++"
  print 'total count ', j
  print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

#  print 
#  print li
#  li = tree.xpath(tab_select)
#  for items in li:
#    if items[UID].text_content().strip() == user:
#      print 'gid: ' + items[GID].text_content().strip()+ ' status: ' + items[STATUS].text_content().strip()
#      print 'title: ' + items[SUBJECT].text_content().strip()
#      print '------------------'

def fetch_content():
 response = urllib2.urlopen('http://outlet.us.dell.com/ARBOnlineSales/Online/InventorySearch.aspx?brandid=1111&c=us&cs=22&l=en&s=dfh&dgc=IR&cid=258996&lid=4635114')
 html = response.read()
 return html 

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
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

