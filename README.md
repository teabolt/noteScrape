# noteScrape
In one sweep download and save all your university or school notes

OR

A collection of scripts for web scraping specific educational resources

## Particular websites and notes to be scraped
* DCU Moodle/Loop (loop.dcu.ie) -> select courses, pdf's
* DCU CA117/CA116 programming websites (ca11X.computing.dcu.ie) -> programs submitted, tasks, site notes

## Main components of a script in this project:
* logging onto the educational platform with the notes (since it's likely exclusive for the educational institution's students)
    * secure storage of credentials (username, password)
* navigating the platform/website, finding the needed content (likely across multiple pages)
    * letting the student mark which notes they want
* downloading/saving the actual notes (pdf, other file type) OR saving the entire page
   * saving links OR the actual content
