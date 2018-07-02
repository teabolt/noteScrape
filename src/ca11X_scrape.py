#!/usr/bin/env python3

"""Web scraper for Dublin City University's modules CA116 and CA117 course websites"""

## Libraries

# Standard
import os # directory creation 
import urllib.parse # manipulate URL's

# Third-party
import requests # HTTP
import bs4 # HTML parser


top_url_ca117 = 'https://ca117.computing.dcu.ie'
top_url_ca116 = 'https://ca116.computing.dcu.ie'


def get_homepage(url, credentials):
    """Retrieve the homepage of a website (based on the url passed), supplying the required credentials
    in CA11X the credentials are a (username, password) tuple"""
    # To-do: security of credentials - not stored plainly in string variables??
    return requests.get(url, auth=credentials)


def retrieve(homepage):
    """Process the entire website, starting from its homepage (a requests object).
    Side effect of saved notes (web pages)"""
    home_soup = bs4.BeautifulSoup(homepage, 'html.parser')
    save(homepage, home_soup)

    links_list = [] # a list wrapper for a stack (with .append(push) and .pop) to get the links in order (most nested first)
    links_set = set() # a filter for links - avoid duplicate links, infinite loops

    home_links = get_links(home_soup)
    links_list += home_links
    links_set.update(home_links)

    while links_list: # while the list is not empty
        link = links_list.pop() # retrieve most recent link
        if link in links_set: # link has been already processed
            continue # skip, move onto the next link

        link_obj = requests.get(link) # get the webpage (HTTP response object)
        save(link_obj, soup=link_soup) # save the page

        link_soup = bs4.BeatifulSoup(link_obj, 'html.parser') # parse the source code
        links_list += get_links(link_soup) # get links from the source code

        links_set.add(link) # add this link to the set of processed links
        # repeat with next most recent link
        

def get_links(soup, base_url=None, tags=False, barebones=True, filt=None):
    """Return the list of all the links on a web page, in the order they appear.
    'soup' is the parsed source code of the web page.
    If 'base_url' is supplied, the links are turned into absolute URL's using 'base_url' as the trunk. ('tags' flag is then assumed to be False)
    If the 'tags' flag is True, the elements (tag objects) that contain the links are returned as opposed to the plain string versions of links. 
    If the 'barebones' flag is True then the only links retrieved are those inside anchor ('<a>') elements with 'href' attributes and that end in '.html'. If the flag is false then all links, including those inside '<link>' elements, as 'src' attributes, and other are retrieved (used for saving a copy of the entire web page including CSS, images, etc)
    If 'filt' is supplied, only those (URL) links with the specified pattern (of 'urllib.parse.ParseResult' object) are returned. (used for only saving hyperlinks 'internal' to the website)"""
    if barebones:
        # find each anchor tag whose 'href' attribute ends in '.html'
        links = soup.select('a[href$=".html"')
        # links pointing to same page (same html) but to a different section of it (with the #ID attribute) are ignored

    if not tags:
        # retrieve the plain links (no tags) 
        links = [link['href'] for link in links]

    if base_url and not tags:
        #  join the (relative) links to the base url's (to make a HTTP request later on)
        urls = []
        for link in links:
            link_url = urllib.parse.urlparse(link)
            if link_url.scheme and link_url.netloc: # if have an application type (http) and a host name
                urls.append(link_url.geturl()) # add the original (likely to be a full absolute url)
            else: # probably a relative link
                urls.append(urllib.parse.urljoin(base_url, link).geturl()) # combine with base url and add the full url
        links = urls # for consistency with the rest of the function

    if filt:
        links = [link for link in links if urllib.parse.urlparse(link)[:2] == filt]
        # include if the application type (http/s) and host name ('ca117.compu..') match

    return links


def save(obj, soup=None):
    """Basic implementation, saves only the html text file.
    Pass parsed HTML of the page if available, else parsing is done here"""
    if soup == None:
        soup = bs4.BeautifulSoup(obj, 'html.parser')

    dir_path = './../notes/ca117/'
    os.makedirs(dir_path, exist_ok=True)

    file_path = dir_path + soup.title.text # use the title for the filename
    with open(file_path, 'wb') as f_out:
        for chunk in obj.iter_content(chunk_size=4294967296): # 32-bits (arbitrary choice)
            f_out.write(chunk)