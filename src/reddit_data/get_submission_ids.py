from datetime import datetime
from pathlib import Path
import praw
from praw.models import Submission
from secrets import CLIENT_SECRET, CLIENT_ID


POST_LIMIT = 1_000_000
DATA_DIR = 'data'
USER_AGENT = 'macos:tone_indicator_scraper:v0.1 (by u/__eel__)'


def read_only_reddit_client() -> praw.Reddit:
    # add params username='' and password='' to get an RW client
    return praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
        ratelimit_seconds=900,  # this is the maxiumum rate limit; by default the max backoff it respects is 4s, but the
                                # api will ask us to backoff as much as 15 mins. Waiting the full backoff period helps
    )                           # ensure that we won't hit a ratelimit exception when issuing requests.
                                # Praw does its network requests through a generator which exits if it hits an exception
                                # even if the exception is handled with try/except. :(


def get_submission_ids():
    print(f'DEBUG [{datetime.now()}]: Starting...')

    if not Path(DATA_DIR).exists():
        raise ValueError(f"Can't find data dir `{DATA_DIR}`. Are you running this from the root of the repository? e.g. `python src/reddit_scraper/scrape.py` from `./LING_573_ND`")

    reddit_client = read_only_reddit_client()
    subreddits = (
        'ADHD',
        'adhdwomen',
        'aspergirls',
        'AutismTranslated',
        'autismmemes',
        'AutisticPride',
        'Autism',
        'AutisticAdults',
        'autisminwomen',
        'neurodivergent',
        'NeurodivergentLGBTQ',
    )

    # For each subreddit, iterate through all submissions and their comments.
    # Write TSV files per subreddit.

    # TODO: any way to make these submission generators resumable between runs?
    for subreddit_name in subreddits:
        print(f'DEBUG [{datetime.now()}]: Getting submission IDs from subreddit {subreddit_name}')

        timestamp = datetime.now().isoformat()

        with open(f'{DATA_DIR}/scraped/{subreddit_name}_post_IDs.txt', 'w') as f:
            submission_ids: list[str] = []

            for submission in reddit_client.subreddit(subreddit_name).new(limit=POST_LIMIT):
                submission: Submission
                if submission.id:
                    submission_ids.append(submission.id)

            lines = '\n'.join(submission_ids)
            f.write(lines)
            print(f'DEBUG [{datetime.now()}]: Found {len(submission_ids)} submissions in subreddit {subreddit_name}')

        print(f'DEBUG [{datetime.now()}]: Finished fetching submission IDs')


if __name__ == '__main__':
    get_submission_ids()
