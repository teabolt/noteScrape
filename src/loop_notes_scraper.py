#!/usr/bin/env python3

"""A web scraper for Dublin City University's Loop/Moodle educational platform notes, 'loop.dcu.ie'"""


## Libraries

# Standard
import os

# Third party

from selenium import webdriver # automatic browser
import requests # http downloads
import bs4 # html parsing


# Utils

def path_build(drive, *args):
        return os.path.join(drive, os.sep, *args)


def all_links(soup):
    """Given a page source (url?), returns a list of all the links on the page"""
    link_tags = soup.find_all(name='a')
    links = []
    for link in link_tags:
        try:
            links.append(link['href'])
        except KeyError:
            print('problem with ', link)
    # need to fix to search only for <a> tags with 'href' attribute
    # or any tag with 'href' attribute?
    return links


def save_site(url):
    """Download a copy of a website with a url, 
    following all the links 'internal' to the site and progressively saving all the pages"""
    pass


# Main

def log_in(url, method='selenium'):
    """Logs onto the educational website. 
    'url' is of the website's very first login page.
    'method' is either 'selenium' or 'requests'.
    Returns an object to be used after the logging-in to interact with the website.
    """

    # authentification
    # ****to be made secure****
    username = input('Your username: ')      
    password = input('Your password: ')

    # selenium solution
    if method == 'selenium':
        # use a simulated browser, click required buttons and fill out required forms (can actually see the browser)
        browser = webdriver.Firefox(executable_path='geckodriver') # requires geckodriver.exe to be in same directory
        browser.get(url)
        # redirect to student login
        dcu_login = browser.find_element_by_css_selector('.btn.btn-success.btn-large')
        dcu_login.click()
        # form login
        username_form = browser.find_element_by_id('username')
        username_form.send_keys(username)
        password_form = browser.find_element_by_id('password')
        password_form.send_keys(password)
        submit_button = browser.find_element_by_css_selector('.form-element.form-button')
        submit_button.click()

        return browser # use this after logging in

    # requests solution
    if method == 'requests':
        # problematic
        # keywords: auth, authentification, form, http, encryption, tcp/ip, ssl, certificate, session
        # https://stackoverflow.com/questions/11892729/how-to-log-in-to-a-website-using-pythons-requests-module
        # http://kazuar.github.io/scraping-tutorial/
        # use Wireshark to monitor http?

        auth_url = 'https://loop.dcu.ie/auth/shibboleth/'
        top_url = 'https://loop.dcu.ie'
        payload = {
        'j_username':'',
        'j_password':''
        }
        s = requests.Session()
        p = s.post(r.url, data=payload)


def get_courses(page_source):
    """Given the HTML source code of a page (for a university learning platform's front page), return a list of tuples, where the first element is the HTTP hyperlink to a course and the second is the title of the course"""
    soup = bs4.BeautifulSoup(page_source, 'html.parser')

    # main box to search inside of which
    modules_box = soup.select_one('div.mymodules_list.mymodules')

    # get the tag element of each module
    # eg: id='course-19175'
    modules = modules_box.select("div[id^='course-']")

    modules_struct = []
    for mod in modules:
        # eg: 'https://loop.dcu.ie/course/view.php?id=19175'
        hyperlink = mod.select_one('a[href*="/course/"]')['href']

        # eg: '\n\n\n\n\n\n\n\nDiscover DCU: A series of short courses\n\n\n\n\n\n\n\n\nAssignment...'
        title_weak_parse = mod.text.strip() # get rid of surrounding whitespace
        right_delim_index = title_weak_parse.find('\n') # assuming whitespace delimits title from the rest of text
        title = title_weak_parse[:right_delim_index] # get rid of text that comes after the title

        modules_struct.append((hyperlink, title))

    return modules_struct


def get_content(hyperlink, title, interactor):
    """Extract and save content of a single entry of a modules_struct element"""

    # create a folder with the title here

    interactor.get(hyperlink)
    soup = bs4.BeautifulSoup(interactor.page_source, 'html.parser')

    # main box where all the course content is
    contents_box = soup.select_one('div.course-content').select_one('ul.topics')

    topics = contents_box.select('li[id^="section-"]')
    # name, resource links, course links, forum links
    topics_struct = []
    for topic in topics:
        # title of the topic
        title = topic['aria-label']

        # resources (pdf's, etc)
        res_tags = topic.select('a[href*="/mod/resource/"]')
        # (link, name) struture
        res_struct = [(res['href'], res.text) for res in res_tags]

        # links to sub-pages of this course (course links)
        # (course name corresponds to topic name)
        course_links = [course['href'] for course in topic.select('a[href*="/course/"]')]

        # forum links
        forum_tags = topic.select('a[href*="/mod/forum/"]')
        forum_struct = [(forum['href'], forum.text) for forum in forum_tags]

        topics_struct.append((title, res_struct, course_links, forum_struct))
    return topics_struct # save this ideally, and follow subsequent links


# def navigate(page_source):
#     """Returns a list of all the links to notes/resources"""

#     # Inside every link

#     content_box = soup.select_one('div.course-content')
#     course_hyperlinks = course_content_box_tag.select('a[href^="http"]')

#     # Inside every link of link

#     # recursion needed, not iteration?
#     # find all resources on page, eg: .pdf links
#     # go to all links and repeat recursively
#     # stop when there's no longer any links
#     # application to find all the links on a page?

#     # link-oriented approach:
#     # get a box tag with all the main content
#     # get all the links
#     # filter the links
#     # follow/do something with the links, based on the link's 'class' (resource, mod, course, etc)


def save_notes(url, interactor, method='selenium'):
    """Saves a piece of notes"""
    # To-do: build a hirearchical filename
    filename = './test-file'

    if method == 'selenium':
        # save the page source
        interactor = browser
        url = browser.current_url
        with open(filename, 'wb') as notes_out:
            notes_out.write(bytes(browser.page_source, encoding='utf-8')) # need to find in meta[charset]

        # does not work for pdf's -> get a blank page with 3 buttons - thumbnails, doc. outline, attachments
        # thumbnails links to original url


# def main():
#     course_element = browser.find_element_by_id('course-9747')
#     # course_link = browser.find_element_by_id('yui_3_17_2_2_1529139101852_1015')
#     course_link = course_element.find_element_by_partial_link_text('MS121')
#     course_link.click()

#     content_element = browser.find_element_by_id('yui_3_17_2_1_1529139169055_107')
#     content_element = browser.find_element_by_id('section-1')
#     content_link = content_element.find_element_by_tag_name('a')
#     content_link.click()

#     all_notes_elem = browser.find_element_by_id('section-1')
#     notes_element = browser.find_element_by_id('module-804127')
#     notes_link = notes_element.find_element_by_tag_name('a')
#     # click and save page

#     # pdf...

#     pdf_url = None
#     pdf_download = browser.find_element_by_id('download')

#     # pdf_src = browser.page_source
#     # soup = bs4.BeautifulSoup(pdf_src, 'html.parser')
#     # txt = soup.select('.textLayer')[0]
#     # with open('D:\\tmp.pdf', 'wb') as f_out:
#     #     f_out.write(txt)

#     # pdf library
#     # 'how to download pdf on web page python' -> link to actual pdf?
#     # headless browser

#     # from xhtml2pdf import pisa
#     # with open('sample_tmp.pdf', 'wb') as pdf_out:
#     #     pisaStatus = pisa.CreatePDF(html, pdf_out)


#     # requests solution here

#     # get all pages and notes here


if __name__ == '__main__':
    main()