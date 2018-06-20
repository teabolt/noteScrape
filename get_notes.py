"""Web scrape school notes"""

## Libraries

# Third party

from selenium import webdriver # automatic browser
import requests # http downloads
import bs4 # html parsing

# Educational platform: 'loop.dcu.ie'

def log_in():
    """Logs onto the educational website.
    Pass auth
    Form"""
    # https://stackoverflow.com/questions/11892729/how-to-log-in-to-a-website-using-pythons-requests-module
    # http://kazuar.github.io/scraping-tutorial/
    # use Wireshark to test?

    auth_url = 'https://loop.dcu.ie/auth/shibboleth/'
    top_url = 'https://loop.dcu.ie'
    payload = {
    'j_username':'',
    'j_password':''
    }
    s = requests.Session()
    p = s.post(r.url, data=payload)


def navigate():
    """Returns a list of all the links to notes/resources"""
    pass

def save_notes():
    """Saves a piece of notes"""
    pass

def main():
    # selenium solution

    browser = webdriver.Firefox(executable_path=r'geckodriver') # requires geckodriver.exe to be in directory
    browser.get('https://loop.dcu.ie')
    dcu_login = browser.find_element_by_css_selector('.btn.btn-success.btn-large')
    dcu_login.click() # redirect

    # need security here
    username_form = browser.find_element_by_id('username')
    username = ''
    username_form.send_keys(username)
    password_form = browser.find_element_by_id('password')
    password = ''
    password_form.send_keys(password)

    submit_button = browser.find_element_by_css_selector('.form-element.form-button')
    submit_button.click()

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

if __name__ == '__main__':
    main()