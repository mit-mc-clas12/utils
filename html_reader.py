#****************************************************************
"""
# Commentary for this file does not yet exist
"""
#****************************************************************


from __future__ import print_function
import utils, fs

def html_reader(url_dir,data_identifier=["",]):
    # create a subclass and override the handler methods
    # from https://docs.python.org/2/library/htmlparser.html
    urls = []

    pyversion = utils.getPythonVersion()
    if pyversion == 2:
        from HTMLParser import HTMLParser #this seems not to work in python3
        import urllib2, argparse
        response = urllib2.urlopen(url_dir) #for python2
    elif pyversion == 3:
        from html.parser import HTMLParser #python 3 version
        from urllib.request import urlopen
        response = urlopen(url_dir) #for python 3, should work but havne't tested this yet (as of 6/1/2020)
    else:
        print("This code only works with python version 2 or 3")
        print("Python version is listed as {0}, please change".format(pyversion))
        exit()

    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            #print("Encountered a start tag: {0}".format(tag))
            pass
        def handle_endtag(self, tag):
            #print("Encountered an end tag: {0}".format(tag))
            pass
        def handle_data(self, data):
            #print("Encountered some data  : {0}".format(data))
            if any([ext in data for ext in data_identifier]):
                urls.append(data)

    raw_html = response.read()
    parser = MyHTMLParser()
    parser.feed(str(raw_html)) #Need to convert bytes to str for python3, should work of for python2 also

    return raw_html, urls


if __name__ == '__main__':
    test_url = "https://www.google.com/"
    data_id = "test_data"
    print(html_reader(test_url,data_id))
