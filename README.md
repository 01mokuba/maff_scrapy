# maff_scrapy

## setup and basic usage

`python 3.6.x` recommended.

1. clone this repository

```
git clone https://github.com/01mokuba/maff_scrapy.git
cd maff_scrapy
```

2. install Scrapy

```
python -m venv .venv
source ./.venv/bin/activate
pip install scrapy
```

3. run the crawler

```
cd maff
scrapy crawl archive -o maff.json --logfile maff.log
```

The results saved in `maff/maff.json` and the log saved in `maff/maff.log`. Downloaded PDFs are saved in `maff/downloads/full`.
