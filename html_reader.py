#****************************************************************
"""
# Commentary for this file does not yet exist
"""
#****************************************************************


from __future__ import print_function
import utils, fs
#from HTMLParser import HTMLParser #this seems not to work in python3
from html.parser import HTMLParser
#import urllib2, argparse
#urllib2 only works for pyton2. For python3 it seems we need to do the following:
from urllib.request import urlopen

def html_reader(url_dir,data_identifyier):
  # create a subclass and override the handler methods
  # from https://docs.python.org/2/library/htmlparser.html
  urls = []
  class MyHTMLParser(HTMLParser):
      def handle_starttag(self, tag, attrs):
          utils.printer2("Encountered a start tag: {0}".format(tag))
      def handle_endtag(self, tag):
          utils.printer2("Encountered an end tag: {0}".format(tag))
      def handle_data(self, data):
          utils.printer2("Encountered some data  : {0}".format(data))
          if data_identifyier in data:
            urls.append(data)

  #response = urllib2.urlopen(url_dir) #for python2
  response = urlopen(url_dir) #for python 3, havne't tested this yet tho
  raw_html = response.read()
  parser = MyHTMLParser()
  parser.feed(raw_html)

  return raw_html, urls
