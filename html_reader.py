#****************************************************************
"""
# Helper function to parse online directorys for lund_helper.py
"""
#****************************************************************



import utils, fs

def html_reader(url_dir,data_identifier=["",]):
    # create a subclass and override the handler methods
    # from https://docs.python.org/2/library/htmlparser.html
    urls = []

    pyversion = utils.getPythonVersion()
    if pyversion == 2:
        from html.parser import HTMLParser # this seems not to work in python3
        import urllib.request, urllib.error, urllib.parse, argparse
        response = urllib.request.urlopen(url_dir) # for python2
    elif pyversion == 3:
        from html.parser import HTMLParser # python3 version
        from urllib.request import urlopen
        response = urlopen(url_dir) # this doesn't work if the url is not public?
    else:
        print("This code only works with python2 or python3")
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
