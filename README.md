# noteScrape

A collection of programs/scripts for scraping/retrieving specific educational (school/university) resources (notes, files, etc) that are on the web (a web scraping application).

**The following are used and required**
* Python 3.7
   * https://www.python.org/
* Python web scraping libraries (selenium, beautifulsoup, requests)
   * ```pip install selenium```
   * ```pip install beautifulsoup4```
   * ```pip install requests```
* Firefox web driver
   * https://github.com/mozilla/geckodriver/releases

The programs are written on a Windows platform so they may not work on other operating systems


## List of scripts, usage

DCU = Dublin City University


### ca1167_scripts_scraper.py 
DCU CA117/CA116 computer programming module student scripts/code (user-submitted to an online checker) retriever

#### Video (click on image to view)

<a href="https://youtu.be/5bRzrB92JoY"
 target="_blank"><img src="http://img.youtube.com/vi/5bRzrB92JoY/0.jpg" 
alt="Image in the middle of the video - showing the browser and the command-line" width="240" height="180" border="10" /></a>

_TO-DO_ Edit the video

#### Usage

##### Before
cmd.exe:
```
cd <project-directory>
cd src
py -3.7 ca1167_scripts_scraper.py ca117 ./../tools/geckodriver ./../output/scripts/ca117/
```

##### Run

The program takes a number of arguments:
1. 'ca117' or 'ca116' (which module)
2. The path of the web browser driver (own or use the supplied driver in tools/)
3. The path of the directory under which all the scripts should be saved


The program runs:
* A particular (Firefox) web browser instance is opened.
* The program asks for the user's credentials via the command-line.
* The program goes through each report page of all the uploaded scripts and saves the code in appropriate '.py' files
* The saved code resides in a directory named with the current date and time, which itself is underneath the directory that was supplied as an argument initially


### _TO-DO_ ca1167_notes_scraper.py
DCU CA117/CA116 computer programming module website notes / site copies maker/saver


### _TO-DO_ loop_notes_scraper.py
DCU Moodle/Loop (loop.dcu.ie) module pdf's/notes/site copies scraper


### _TO-DO_ generic_scraper.py
Common patterns for web scraping


## Development notes

### Main components of a script in this project:
* logging onto the educational platform with the notes (since it's likely exclusive for the educational institution's students)
    * secure storage of credentials (username, password)
* navigating the platform/website, finding the needed content (likely across multiple pages)
    * letting the student mark which notes they want
* downloading/saving the actual notes (pdf, other file type) OR saving the entire page
   * saving links OR the actual content


### Questions for clarity
* if you want to scrape data off a website, what data do you want exactly?
   * if you want 'anything that could be useful', what types of things would be 'useful'?
   * if you want 'notes', what kinds of notes do you want, pdf's, word documents?
   * if you want coursework details, do you want both your submissions and the specifications of the work?
   * do you actually just want an exact copy of the web page saved?
   * do you want a partial copy of the web page?
* where do you want to get the data from?
   * do you want to get the data from every corner of every page you can access ever?
   * how will you traverse the web page, with recursion or iterating through layers?
   * if you limit the scope of your sources, how? What decides whether something makes into the list of 'sources' and not?
   * are there common threads and patterns among the sources from which you want to scrape? Any exceptions?
* how will you save the data?
   * html source code allowing you to view pdf's in browser, but how to actually get the pdf's?
