#!/usr/bin/env python3

"""A web scraper for retrieving the uploaded scripts to the Dublin City University's module websites CA116 and CA117. 
Uploads are done to an online checker 'Einstein', that provides reports and a summary of uploaded scripts for associated programming 'tasks'."""

## Libraries

# Standard

import os # directory creation
import os.path # file path creation
import urllib.parse # manipulation and analysis of URL's
import datetime # dates and times
#import time # timestamps
import sys # system arguments

# Third-party

import requests # HTTP lib
#import bs4 # parse HTML
# selenium - automated browser
#import selenium
from selenium import webdriver # virtual/automated browser
from selenium.webdriver.common.keys import Keys # press special keyboard keys
from selenium.webdriver.support.ui import WebDriverWait # wait for events/for some time
from selenium.webdriver.support import expected_conditions as EC # until some condition
from selenium.webdriver.common.by import By # get elements by id, css selector, etc


# Need to make the decision about whether to use selenium or beautifulsoup to parse HTML. 
# Perhaps selenium is basic but gets the job done and using it only simplifies things. 
# beautifulsoup may be for more advanced parsing of which I am not aware of yet.


ca117_globals = {
    'dashboard_url':'https://ca117.computing.dcu.ie/einstein/task-dashboard.html?user=baltrut2',
    'base_url':'https://ca117.computing.dcu.ie',
}

ca116_globals = {
    'dashboard_url':'https://ca116.computing.dcu.ie/einstein/task-dashboard.html?user=baltrut2',
    'base_url':'https://ca116.computing.dcu.ie'
}

default_env_globals = {
    'driver_path':r'D:/Development/noteScrape/tools/geckodriver',
    'save_dir_path':r'D:/Development/noteScrape/output/scripts/',
}


# def requests_scrape():
#     """Broken. Do not use."""
#     raise NotImplemented
#     t1 = time.time()
#     ses = requests.Session()
#     print('created session object {}'.format(ses))
#     auth_credentials = (input('user: '), input('pw: ')) # make secure
#     home_url = 'https://ca117.computing.dcu.ie/einstein/task-dashboard.html'
#     res_home = ses.get(home_url, auth=auth_credentials)
#     print('Requested homepage {}, got object {}'.format(home_url, res_home))
#     res_home.raise_for_status(); assert res_home.status_code == 200
#     print('Got response with code {}, some text {}'.format(res_home.status_code, res_home.text[:250]))
#     soup_home = bs4.BeautifulSoup(res_home.text, 'html.parser')
#     print('Parsed HTML, {}'.format(soup_home.text[:250]))
#     tasks_box = soup_home.select_one('ul#outerList')
#     print('Focusing on a container element {}'.format(tasks_box.text[:250]))
#     try:
#         link_tags = tasks_box.select('a[class="uploadIconContainer"][target="einsteinUploadWindow"][title*="report"]')
#     except ValueError:
#         link_tags = tasks_box.select('a.uploadIconContainer')
#     print('Got {} "a" tags, {}'.format(len(link_tags), link_tags[:5]))
#     links = [tag['href'] for tag in link_tags]
#     print('Extracted {} "href" contents, {}'.format(len(links), links[:5]))
#     base_url = 'https://ca117.computing.dcu.ie'
#     urls = [urllib.parse.urljoin(base_url, link) for link in links]
#     print('Constructed {} URLs, {}'.format(len(urls), urls[:5]))
#     t2 = time.time()
#     print('Took {} seconds'.format(t2-t1))

#     curr_time = datetime.datetime.now()
#     path_out = os.path.join('D:/', 'Development/noteScrape/notes/{}/'.format(curr_time.strftime('%Y%m%d%H%M%S')))
#     os.makedirs(path_out, exist_ok=True)
#     print('Created directory {}'.format(path_out))

#     print('Going through each URL')
#     t3 = time.time()
#     print('---')
#     for url in urls:
#         try:
#             print('Started new task')
#             res_task = ses.get(url, auth=auth_credentials)
#             #res_Task.raise_for_status(); assert res_task.status_code == 200
#             print('Got a task with url {}, into response object {}, with status code {}, and some text {}'.format(url, res_task, res_task.status_code, res_task.text[:250]))
#             soup_task = bs4.BeautifulSoup(res_task.text, 'html.parser')
#             print('Parsed HTML, with text {}'.format(soup_task.text[:250]))
#             code_box = soup_task.select_one('pre#upload')
#             print('Targetting element with the code, {}'.format(code_box.text[:250]))
#             sourcecode = code_box['data-clipboard-text']
#             print('Got the source code, {}'.format(sourcecode[:250]))
#             url_p = urllib.parse.urlparse(res_task.url) # 'date=2018-05-15&task=minelts_112.py&user=baltrut2'
#             params = url_p.query.split('&')
#             task_date = params[0].split('=')[1] # repeated code for a group of tasks?
#             task = params[1].split('=')[1]
#             with open(os.path.join(path_out, task), 'wb') as f_out:
#                 out = f_out.write(bytes(sourcecode, encoding='utf-8'))
#                 print('Saved {} bytes'.format(out))
#         except Exception as exc:
#             print('Skipping a task, {} has occurred'.format(exc))
#         finally:
#             print('Finished this task')
#             print('-'*10)

#     print('Finished all')
#     t4 = time.time()
#     print('Took {} seconds'.format(t4-t3))

# requests_scrape did not work because 'requests' doesn't seem to be able to fetch the full HTML pages of ca117 (contents missing, only outline/help text returned). 'selenium' works as it loads the entire page with all its contents, and then the HTML source can be observed.


def selenium_scrape(dashboard_url, base_url, driver_path, save_dir_path):
    """Save all the code that can be found in a web dashboard listing all scripts that were uploaded 
    using a selenium automated browser"""
    browser = webdriver.Firefox(executable_path=driver_path)
    browser.get(dashboard_url)

    # login pop-up window solution from: 
    # https://stackoverflow.com/questions/41819749/python3-selenium-fill-username-and-password-in-popup-dialog
    # https://www.google.com/search?client=firefox-b-ab&ei=nkNPW7OzH6iC8gKDooPwCg&q=selenium+get+page+with+password+python+login+-form+dialog+box&oq=selenium+get+page+with+password+python+login+-form+dialog+box&gs_l=psy-ab.3...10162.11514.0.11668.11.11.0.0.0.0.117.948.9j2.11.0....0...1c.1.64.psy-ab..0.0.0....0.nfH0MTbawP4
    # https://developer.mozilla.org/en-US/docs/Web/API/Window/alert
    # point at alert immediatelly? But need to wait some time for the alert to appear? Alert from server, not in HTML page?
    # *access* alert object immediatelly? Not as an expected condition happening but as an element?
    # <class 'selenium.webdriver.common.alert.Alert'>
    alert = WebDriverWait(browser, 5).until(EC.alert_is_present()) # what should be the wait time?
    alert.send_keys(input('Username: ')+Keys.TAB+input('Password: ')) # (no spaces, concatinate)
    alert.accept()
    # security needed with inputting and saving locally of credentials

    # replace beautifulsoup parsing with selenium parsing
    # also include waits - contents are probably gotten from server - wait a bit, else get a NoneType object
    # more rigorous implementation - else need to keep trying? OR always fail?

    #dashboard_src = browser.page_source
    #dashboard_soup = bs4.BeautifulSoup(dashboard_src, 'html.parser') # use Selenium instead of BeautifulSoup?
    #tasks_box = dashboard_soup.select_one('ul#outerList')
    #link_tags = tasks_box.select('a.uploadIconContainer')
    #links = [tag['href'] for tag in link_tags]

    tasks_box = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul#outerList')))
    link_tags = tasks_box.find_elements_by_css_selector('a.uploadIconContainer')
    links = [tag.get_attribute('href') for tag in link_tags]
    # is the step below needed? links seem to be URL's already? Check if 'is_url' first somehow to save computations?
    urls = [urllib.parse.urljoin(base_url, link) for link in links]

    curr_time = datetime.datetime.now()
    path_out = os.path.join(save_dir_path, '{}/'.format(curr_time.strftime('%Y%m%d%H%M%S')))
    os.makedirs(path_out, exist_ok=True)

    task_no = len(urls)
    i = 0
    for task_url in urls:
        get_task(browser, task_url, path_out)
        # Originally solved the problem of a KeyError from missing element by catching it, refreshing the browser, and calling 'get_task()' with the needed arguments again.
        # Worked at first, but sometimes doesn't as another KeyError is thrown despite the refresh (need multiple refresh calls / recursion / nesting?)
        # Hypothesis is that the web server needs time to respond with the contents of the 'pre#upload' tag (its contents come later than the HTML page OR a different server handles the uploaded files, while another handles the HTML pages / templating). This was fixed by using Selenium waits for the 'pre#upload' tag *with* its 'data-clipboard-text' content (or any content can be waited for really)
        # Handle a timeout exception?
        # Skip a task and 'mark' it? Return to it later? Access non-sequentially?

        # Manual downloading of page? - get info on it and use 'get_task()' yourself? 
        # Get an iterator on the URLs with iter(), and use next()?
        i += 1
        print('{0}  DONE {1} / {2}  {0}'.format('*'*10, i, task_no))     
        print('-'*20)
        # TO-DO: proper debug messages / options

    # let user do own timing when calling the function / program, don't time things internally


def get_task(browser, task_url, path_out):
    """Retrieve and save the code of a script using its upload report URL, via a selenium browser"""
    browser.get(task_url); print('URL: ', task_url)
    task_src = browser.page_source; print('Source:', task_src[:250])

    #task_soup = bs4.BeautifulSoup(task_src, 'html.parser'); print('Soup: ', task_soup.text[:250])
    #code_box = task_soup.select_one('pre#upload')
    # using selenium instead of beautifulsoup

    code_box = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'pre#upload[data-clipboard-text]'))); print('Code box: ', code_box.text[:250])
    # 'presence_of_ele...' takes a tuple as an argument
    # wait time?
    # http://selenium-python.readthedocs.io/waits.html
    code = code_box.get_attribute('data-clipboard-text'); print('Code: ', code[-250:])

    task_url_p = urllib.parse.urlparse(task_url)
    params = task_url_p.query.split('&'); print(params)
    task_date, task_name, task_user = [q.split('=')[1] for q in params]
    # 'task_user' will not be used

    code_path_out = os.path.join(path_out, task_date); print(code_path_out)
    os.makedirs(code_path_out, exist_ok=True)
    with open(os.path.join(code_path_out, task_name), 'wb') as f_out:
        ch = f_out.write(bytes(code, encoding='utf-8'))
        print(ch)


# Giving the server a break / not being rate limited is important. Perhaps time.sleep() should be incorporated.
# What times should selenium waits take? 5 seconds?

# async? Separate requesting and receiving web pages, parsing them, and saving the results?

# Generalise - control what to download / index tasks
# ca116 support
# more general specifics, eg: specific HTML elements pointed at

# browser changes windows fast and automatically "does stuff" - damn what a show! HackerMan!

# have order with folder dates, but lacking 'internal' order within folders

# sometimes it takes some time to get a page (loading icon keeps on spinning), so perhaps some timeout-wait-retry mechanism is needed to make things more rigorous (else can just time out in the middle of things)


def main():
    """Takes three command-line arguments
    'which' is either 'ca117' or 'ca116' (two different modules)
    'driver_path' is the path (with forward slashes '/') of the geckodriver.exe program for selenium, with '/geckodriver' at its end
    'save_dir_path' is the path (with forward slashes '/') of the directory where the notes should be saved, starting with a drive path 'X:/' (for Windows) and ending with a forward slash '/'"""
    args = sys.argv[1:]
    assert len(args) == 3
    which = args[0]
    env = {'driver_path':args[1], 'save_dir_path':args[2]}

    if which == 'ca117':
        selenium_scrape(**ca117_globals, **env)
    elif which == 'ca116':
        selenium_scrape(**ca116_globals, **env)


if __name__ == '__main__':
    main()