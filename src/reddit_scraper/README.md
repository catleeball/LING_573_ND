# Reddit Scraper

Script to scrape posts from reddit and analyze possible tags

## Usage

- Ensure you're in the root of the repo `./LING_573_ND`
- Activate venv (e.g. `source .venv/bin/activate`)
- If needed, install praw and requests
  - `pip install praw requests`
- Define the following in `src/reddit_scraper/secrets.py` for your reddit API connection
  - CLIENT_ID = ''
  - CLIENT_SECRET = ''
- Run
  - `python src/reddit_scraper/scrape.py`
- Logs are written to root directory
- Data is written to `data/scraped/` in a .bz2 file
