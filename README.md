# Roppers Thinkific Scraper

## Install
Clone repo
```bash
git clone git@github.com:cblanken/roppers-thinkific-scraper.git; cd roppers-thinkific-scraper
```

Install dependencies
```bash
pip install -r requirements.txt
```

You'll also need to install [`pandoc`](https://pandoc.org/installing.html) to use the `convert.py` script.

## Usage
Scraper
```
Usage: python ./scrape.py <course_url> <save_dir>
For example: python ./scrape.py  https://www.roppers.org ComputingFundamentals
Provide login creds via env vars THINKIFIC_USER and THINKIFIC_PASS
```
