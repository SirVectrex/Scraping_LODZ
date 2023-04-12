# Webscraper for LODZ

This is a webscraper for the public library of Lodz, Poland.
The official website can be found [here](http://www.biblioteka.lodz.pl/) and their open database [here](http://bc.wimbp.lodz.pl/dlibra).

## Usage

1. Make sure you have Python installed on your machine. Then run the following commands for setup: 
```bash
    pip install -r requirements.txt
    python scraper.py
```

2. Find out what kind of magazines or book you want to look for and edit following lines in main.py

```python

start = 30000 # start scraping at this document number
end = 30700 # end scraping at this document number
max_jobs = 80 # number of threads to maximum use
searchable_article = "Freie Presse" # search for this article in the title

```

NOTE: 
- The scraper will only scrape documents with the given text in the title. 
- Use maximum thread with caution (100 max on i7 4900K).
- Use Start and End to limit the number of searches. Maybe manually find the first and last element.

## Logging and Output

1. All files will be saved in the folder "downloads".
2. Two log fileswill be saved in the folder "logs".
- Misses.txt documents all documents that were found, but not of relevance
- Hits.txt documents all documents that were found and of relevance

