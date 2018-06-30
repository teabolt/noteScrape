#!/usr/bin/env python3

"""Web scraper for Dublin City University's modules CA116 and CA117 course websites"""

import requests
import bs4

top_url_ca116 = 'https://ca116.computing.dcu.ie'
top_url_ca117 = 'https://ca117.computing.dcu.ie'

# To-do: security??
def log_in(url, username, password):
    """Retrieve a page with a url by supplying credentials"""
    return requests.get(url, auth=(username, password))

# Retrieve all resources to completely load the page
def get_links(page_src):
    """For a web page with a source code, return a list of all the links (precisely the elements that contain links) on the page, including elements with 'href' and 'src' attributes"""
    pass

# Save only bare-bones hyperlinks, 'internal' to the website.
def save_hyperlinks(page_src):
    """str: source code -> list: all anchor 'a' elements with a specific pattern for the URL or 'href' value"""
    pass