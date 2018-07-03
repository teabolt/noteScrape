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
    """Retrieve/download the homepage of a website (based on the url passed), supplying the required credentials
    (in CA11X the credentials are a (username, password) tuple)
    A requests response is returned."""
    # To-do: security of credentials - not stored plainly in string variables??
    return requests.get(url, auth=credentials)


def process(homepage):
    """Retrieve/download the entire website, starting from its homepage (a requests object).
    Side effect of saved notes (web pages)"""
    home_soup = bs4.BeautifulSoup(homepage, 'html.parser')
    save(homepage, home_soup)

    links_list = [] # a list wrapper for a stack (with .append(push) and .pop) to save and get the links in order (most nested first)
    links_set = set() # a filter for links already processed - avoid duplicate links, infinite loops, etc

    home_links = get_links(home_soup)
    links_list += home_links

    while links_list: # while the list is not empty (still have links)
        link = links_list.pop() # get the most recent link
        if link in links_set: # check if link has not been already processed
            continue # skip, move onto the next link

        link_res = requests.get(link) # get the web page (HTTP response object)
        save(link_res, soup=link_soup) # save the web page

        link_soup = bs4.BeatifulSoup(link_obj, 'html.parser') # parse the web page's source code
        # get links from the page's source code
        # and add them to to-be processed links 
        links_list += get_links(link_soup, base_url=homepage.url)

        links_set.add(link) # add this link to the set of processed links (or use .update(iterable))
        # repeat with next most recent link


def get_links_bare(soup, tags=False):
    """Return a list of all the links on a web page based on its source code that has been parsed.
    The operation is 'bare' in that the only 'links' retrieved are those inside anchor ('<a>') elements 
    with 'href' attributes that begin in 'http' or end in '.html'.
    If the 'tags' flag is True, the elements (tag objects) that contain the links are returned, 
    as opposed to the plain string versions of links.
    eg: Tag object <a href="..."></a> is returned instead of just the contents of 'href'.
    """

    # find each anchor tag whose 'href' attribute *ends in* '.html' OR (inclusive) *begins with* 'http'(/s)
    # links pointing to same page (same html) but to a different section of it (#ID attribute) are ignored
    links = soup.select('a[href^="http"], a[href$=".html"]')
    # TO-DO: regex 'https?://'

    if not tags:
        links = [link['href'] for link in links] # retrieve the plain links (no tags)
    return links

    # problem - links retrieved out of order (though order is desirable), some missing (duplicate?)


def get_full_links(soup, tags=False):
    """Return a list of *all links* on a web page based on its parsed source code, 
    including those links inside '<link>' elements, as 'src' attributes, and so on.
    If tags is True the elements containing the links are returned, else only links as text are returned.
    Use for saving a copy of the entire web page including CSS, images, etc."""
    # TO-DO: get an official reference of all 'links' possible in HTML
    raise NotImplemented


def get_urls(links, base_url):
    """Turn a list of 'href' links into URL's. Relative or partial links are turned into absolute URL's using 'base_url' as the trunk (often the URL of the homepage, but not the 'top level' URL)
    Use to make HTTP requests for those URL's
    """
    urls = []
    for link in links:
        link_url = urllib.parse.urlparse(link) # parse the link as a URL
        if link_url.scheme and link_url.netloc: # if have an application type (http/s) and a host name
            urls.append(link_url.geturl()) # add the original (likely to be a full absolute url)
        else: # probably a relative link
            urls.append(urllib.parse.urljoin(base_url, link)) # combine relative and base url's
    return urls

    # problem - when relative navigation is used ('../../'), URL's are built with missing parent directories


def filter_urls(urls, filt=None):
    """Filter a list of URL's based on 'filt'. A sub-list of 'urls' is returned.
    'filt' is a dictionary mapping from attribute names (strings) of 'urllib.parse.ParseResult'
    to values (strings) of those attributes.
    The value may be a single string value or a list of string values of which each at least one must match.
    The values are compared *strictly* (==)
    eg: Use when only want to save hyperlinks 'internal' to the website:
    include if the application type (http/s) and host name ('ca117.computing.dcu.ie') match,
    filt = {'scheme':['http', 'https'], 'netloc':'ca117.computing.dcu.ie'}
    """

    if filt == None:
        return urls

    filtered_urls = []
    for url in urls:
        print(url)
        parsed_url = urllib.parse.urlparse(url)
        print(parsed_url)
        for attr in filt.keys(): # go through each attribute (scheme, host, path, etc)
            val = filt[attr] # the required value for this attribute
            print(val)
            # (using type checking to direct control flow - there might be better ways)
            # NOT type(val) == type(str), RHS is type 'type'
            if type(val) == str: # a single value was specified
                print('here1')
                print(getattr(parsed_url, attr))
                if val == getattr(parsed_url, attr):
                    filtered_urls.append(url)
                else:
                    break # 1 attribute doesn't match, skip this URL
            elif type(val) == list: 
                print('here2')
                for v in val: # go through each value in the list of allowed values
                    print(v, getattr(parsed_url, attr))
                    if v == getattr(parsed_url, attr):
                        filtered_urls.append(url)
                    # TO-DO: break if none of the values match
                        break # finished (only one required value needs to match)
            else:
                pass
                print('here3')
                # anything else in the filt dict is ignored
    return filtered_urls
    # TO-DO: list of attributes, pass integers as attributes, helpful messages for users
    # match by substring/containment
    # catch AttributeError's (supplied wrong attributes / dict keys)


def save(obj, soup=None):
    """Basic implementation, saves only the html text file.
    Pass the parsed HTML of the page if can, otherwise parsing is done inside the function"""
    if soup == None:
        soup = bs4.BeautifulSoup(obj, 'html.parser')

    dir_path = './../notes/ca117/'
    os.makedirs(dir_path, exist_ok=True)

    file_path = dir_path + soup.title.text # use the title as the filename
    with open(file_path, 'wb') as f_out:
        for chunk in obj.iter_content(chunk_size=4294967296): # 32-bits (arbitrary choice)
            f_out.write(chunk)


def main():
    res = get_homepage(top_url_ca117, (input('name: '), input('pw: ')))
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    links = get_links(soup, base_url=top_url_ca117)
    return soup, links

if __name__ == '__main__':
    main()