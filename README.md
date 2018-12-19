# ocho_scraper

<p align="center">
<img src="ocho_preview.gif" alt="animated gif of ocho_scraper functionality" />
</p>



## installation

**clone repo**

```
git clone git@github.com:pungprakearti/ocho_scraper.git
```

**change directory into repo**

```
cd ocho_scraper
```

**create secret file**

```
touch secret.py
```

**edit secret file with URLs to scrape**

Use whichever editor you prefer.
The syntax inside the secret.py is:

```python
url1 = "http://www.google.com"
url2 = "http://www.yahoo.com"
```

---

## running the scraper

```
python3 ocho_scraper.py
```

**remove local saved data and rescrape all**

This is an optional step. Sometimes the instructors have typos or change code after you've already scraped it. Use this command to rescrape **everything**. If you want to scrape individual files, just delete the directory for the lecture/exercise and when you run ocho_scraper without -a, it will rescrape that specific folder.

```
python3 ocho_scraper.py -a
```

---

## open the indexer

```
open index.html
```

Use command + f to search for keywords in the indexer and the links will take you right to where the information lives.

---

## profit

![burning money](https://gif-free.com/uploads/posts/2017-04/1492691196_frank-reynolds-money.gif)

## COHORT OCHO FOREVER!!!
