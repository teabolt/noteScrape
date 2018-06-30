# noteScrape
In one sweep download and save all your university or school notes

OR

A collection of scripts for scraping specific educational resources that are on the web

## Particular websites and notes to be scraped
DCU = Dublin City University
* DCU Moodle/Loop (loop.dcu.ie) -> select courses, pdf's
* DCU CA117/CA116 programming websites (ca11X.computing.dcu.ie) -> programs submitted, tasks, site notes

## Main components of a script in this project:
* logging onto the educational platform with the notes (since it's likely exclusive for the educational institution's students)
    * secure storage of credentials (username, password)
* navigating the platform/website, finding the needed content (likely across multiple pages)
    * letting the student mark which notes they want
* downloading/saving the actual notes (pdf, other file type) OR saving the entire page
   * saving links OR the actual content

## Questions for clarity
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
   
