#!/usr/bin/env python3

"""A generic web scraper class that tries to abstract and wrap many commonly used web scraping code patterns"""

## Libraries

# Standard
import os # directory creation 
import urllib.parse # manipulate URL's
import re # match patterns

# Third-party
import requests # HTTP
import bs4 # HTML parser


class Scraper():
    
    def __init__(self, base_url):
        self.base_url = ''

    def requests_session(self):
        pass

    def items_from_homepage(session, homepage=None, item=None, limiting_box=None):
        pass

    def link_from_item():
        pass

    def data_from_item():
        pass

    def folders():
        pass

    def data_save():
        pass


def main():
    ca117 = Scraper(base_url='https://ca117.computing.dcu.ie')
    central_page = ca117.central_page()



if __name__ == '__main__':
    main()