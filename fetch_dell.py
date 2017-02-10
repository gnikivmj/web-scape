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
import json

sleep_time = 300
long_sleep = 60 * 30
"""
json sample:
  {
    "key": "key",
    "sandbox": "sandbox",
    "recipient": "example@example.com",
    "filter": "7310"
  }
"""
class dell_parser:
  def __init__(self, config_file="fetch_dell.json"):
    self.config = config_file
    self.load_config()

  def load_config(self):
    with open(self.config, "r") as input:
      c = input.read()
      print c
      self.json = json.loads(c)

  def print_config(self):
    print self.json

  def send_mail(self, content=None):
    request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(self.json['sandbox'])
    text = 'Hello from Mailgun'
    if content:
      text = content

    request = requests.post(request_url, auth=('api', self.json['key']), data={
      'from': 'dell@mailgun.org',
      'to': self.json['recipient'],
      'subject': 'Dell Outlet Alert',
      'text': text
      })

    print 'Status: {0}'.format(request.status_code)
    print 'Body:   {0}'.format(request.text)

  def parse_content(self, content):
    tree = html.fromstring(content)
    tab_select = '//table[@class="fl-width100 fl-topline"]'
    li = tree.xpath(tab_select)
    #print tab_select
    #print li
    j = 0
    content = ""
    for items in li:
      j += 1
      title = items.find_class('fl-inv-head')[0].text_content().strip()
      if self.json['filter'] in title:
        #print title
        price = items.find_class('fl-inv-price')[0].text_content().strip()
        #print price
        details = items.find('tr/td/ul')
        detail = ""
        for d in details:
          detail += d.text_content().strip() + "\r\n"
        #print detail
        #print "++++++"
        content += title + "\r\n\r\n" + detail + "\r\n" + price + "\r\n" + "++++++++++++++++++++\r\n\r\n"

    print content
    print 'total count ', j
    print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

    #search for the family to double check if it has the item listed
    if content == "":
      default = []
      family = tree.get_element_by_id('itemheader-FN', default)
      for type in family:
        type_name = type.text_content().strip()
        if self.json['filter'] in type_name:
          content += "find type: " + type_name + "\r\n"

    if content != "":
      content += self.json['url'] + '\r\n\r\n'
      content += time.ctime() + '\r\n'
      self.send_mail(content)
      return content

    return None


  def fetch_content(self):
    try:
      response = urllib2.urlopen(self.json['url'])
      html = response.read()
      return html
    except:
      print "Error on open url..."
      return None


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  if len(sys.argv) >= 2:
     option  = sys.argv[1]
  else:
     option = None

  d = dell_parser()
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
    #d.print_config()
    while True:
      print "fetch content ...", time.ctime()
      content = d.fetch_content()
      st = sleep_time
      if content is not None:
        print "parsing ...", time.ctime()
        find = d.parse_content(content)
        if find is not None:
          st = long_sleep
      print time.ctime(), "sleep for %ss" % st
      time.sleep(st)
"""
ipython test codes:

import codecs
f = codecs.open("dell.html", 'r', 'utf-8')
content = f.read()
from lxml import html
tree = html.fromstring(content)
tab_select = '//table[@class="fl-width100 fl-topline"]'
li = tree.xpath(tab_select)
item = li[0]
price = items.find_class('fl-inv-price')[0].text_content().strip()

"""
