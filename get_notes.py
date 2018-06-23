"""Web scrape school notes"""

## Libraries

# Standard
import os

# Third party

from selenium import webdriver # automatic browser
import requests # http downloads
import bs4 # html parsing

# Particular educational platform for now: 'loop.dcu.ie'

def log_in(url, method='selenium'):
    """Logs onto the educational website. 
    'url' is of the website's very first login page.
    'method' is either 'selenium' or 'requests'.
    Returns an object to be used after the logging-in to interact with the website.
    """

    # selenium solution
    if method == 'selenium':
        # use a simulated browser, click required buttons and fill out required forms (can actually see the browser)
        browser = webdriver.Firefox(executable_path='geckodriver') # requires geckodriver.exe to be in same directory
        browser.get(url)
        # redirect to student login
        dcu_login = browser.find_element_by_css_selector('.btn.btn-success.btn-large')
        dcu_login.click() 

        # form login
        # ****to be made secure****
        username_form = browser.find_element_by_id('username')
        username = input('Your username: ')      
        username_form.send_keys(username)
        password_form = browser.find_element_by_id('password')
        password = input('Your password: ')
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

def navigate():
    """Returns a list of all the links to notes/resources"""

    ## Home page
    # modules_box = soup.select('.mymodules_list.mymodules')[0]
    # modules = modules_box.select("div[id^='course-']")
    # links = [module.select(".course_title a[href^='https://loop.dcu.ie']")[0]['href'] for module in modules]

    # OR

    modules_box_tag = soup.select_one('div.mymodules_list.mymodules') # main box for where to search inside
    modules_hyperlink_tags = modules_box_tag.select('a[href*="/course/"]')
    modules_hyperlinks = [a_tag['href'] for a_tag in module_hyperlink_tags]

    # Inside every link

    course_content_box_tag = soup.select_one('div.course-content')
    course_hyperlinks = course_content_box_tag.select('a[href^="http"]')

    # Inside every link of link

    # recursion needed, not iteration?
    # find all resources on page, eg: .pdf links
    # go to all links and repeat recursively
    # stop when there's no longer any links
    # application to find all the links on a page?

    # link-oriented approach:
    # get a box tag with all the main content
    # get all the links
    # filter the links
    # follow/do something with the links, based on the link's 'class' (resource, mod, course, etc)

def save_notes(url, method='selenium', interactor):
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

def main():

    course_element = browser.find_element_by_id('course-9747')
    # course_link = browser.find_element_by_id('yui_3_17_2_2_1529139101852_1015')
    course_link = course_element.find_element_by_partial_link_text('MS121')
    course_link.click()

    content_element = browser.find_element_by_id('yui_3_17_2_1_1529139169055_107')
    content_element = browser.find_element_by_id('section-1')
    content_link = content_element.find_element_by_tag_name('a')
    content_link.click()

    all_notes_elem = browser.find_element_by_id('section-1')
    notes_element = browser.find_element_by_id('module-804127')
    notes_link = notes_element.find_element_by_tag_name('a')
    # click and save page

    # pdf...

    pdf_url = None
    pdf_download = browser.find_element_by_id('download')

    # pdf_src = browser.page_source
    # soup = bs4.BeautifulSoup(pdf_src, 'html.parser')
    # txt = soup.select('.textLayer')[0]
    # with open('D:\\tmp.pdf', 'wb') as f_out:
    #     f_out.write(txt)

    # pdf library
    # 'how to download pdf on web page python' -> link to actual pdf?
    # headless browser

    # from xhtml2pdf import pisa
    # with open('sample_tmp.pdf', 'wb') as pdf_out:
    #     pisaStatus = pisa.CreatePDF(html, pdf_out)


    # requests solution here

    # get all pages and notes here


def path_build(drive, *args):
        return os.path.join(drive, os.sep, *args)

if __name__ == '__main__':
    main()