#****************************************************************
"""
# Commentary for this file does not yet exist
"""
#****************************************************************


from __future__ import print_function
import utils, file_struct
from HTMLParser import HTMLParser
import urllib2, argparse

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

  response = urllib2.urlopen(url_dir)
  raw_html = response.read()
  parser = MyHTMLParser()
  parser.feed(raw_html)

  return raw_html, urls
