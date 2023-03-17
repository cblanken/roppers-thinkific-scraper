# Roppers Thinkific Scraper

## Download
```bash
git clone git@github.com:cblanken/roppers-thinkific-scraper.git; cd roppers-thinkific-scraper
```

Install dependencies
```bash
pip install -r requirements.txt
```
Install [`pandoc`](https://pandoc.org/installing.html) to use the `convert.py` script.

## Usage
Scraper
```
Usage: python ./scrape.py <course_url> <save_dir>
For example: python ./scrape.py  https://www.roppers.org ComputingFundamentals
Provide login creds via env vars THINKIFIC_USER and THINKIFIC_PASS
```

Pandoc converter (HTML to Markdown)
```
Usage
-------------------------------------------------
Convert HTML files from <course_dir> into Markdown files in <out_dir>
$ python ./convert.py <course_dir> <out_dir>
-------------------------------------------------
Same as above but re-embed iframe tags at the start of Markdown output file.
$ EMBED_IFRAME=1 python ./convert.py <course_dir> <out_dir>
```
