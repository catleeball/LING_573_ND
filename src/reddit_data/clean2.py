import json
import string

from joblib import Parallel, delayed
from pyzstd import ZstdFile
import re
from urlextract import URLExtract


JOB_COUNT = 24
DEBUG_DATA_FILE = '/Media/Data/reddit/first_100.json.zst'
DATA_FILE = '/Media/Data/reddit/nd_subreddits.json.zst'
OUTPUT_FILE = '/Media/Data/reddit/data_cleaned_and_filtered.json'
SARCASM_REGEX = re.compile(r'(/s[\s$,.?!]|/sarcasm[\s$,.?!]|/sarcastic[\s$,.?!])')
SERIOUS_REGEX = re.compile(r'(/serious[\s$,.?!]|/srs[\s$,.?!])')

# Mutable global vars for stats collection (sorry)
sarcasm_count = 0
serious_count = 0
bad_input_str = 0
validate_json_failed = 0
post_deleted = 0
post_removed = 0
contains_url = 0
no_tone = 0


def validate_json(json_dict: dict | None) -> dict | None:
    """Drop json objects that don't have a useful `selftext` attribute"""
    if not json_dict:
        return None
    if 'selftext' not in json_dict:
        return None

    global validate_json_failed

    text: str | None = json_dict['selftext']

    match text.strip():
        case None:
            validate_json_failed += 1
            return None
        case '':
            validate_json_failed += 1
            return None
        case '[deleted]':
            global post_deleted
            post_deleted += 1
            return None
        case '[removed]':
            global post_removed
            post_removed += 1
            return None
        case _:
            return json_dict


def clean_text(json_dict: dict | None) -> dict | None:
    if not json_dict:
        return None

    text: str = json_dict['selftext']
    text = text.strip()
    # Remove non-ASCII characters from json's selftext
    text = str(filter(lambda c: c in string.printable, text))

    # Remove URLs from json's selftext
    url_extractor = URLExtract()
    # Get unique URLs in document text
    urls = set()
    for url in url_extractor.gen_urls(str(text)):
        urls.add(url)
    if len(urls) > 0:
        global contains_url
        contains_url += 1
    if urls:
        for url in urls:
            text = text.replace(url, '')

    json_dict['selftext'] = text
    return json_dict


def tone_indicator_filter_and_labeler(json_dict: dict | None) -> dict | None:
    """Remove jsons that don't contain tone indicators. Add json entries indicating those that do."""
    if not json_dict:
        return None

    is_sarcastic = bool(re.search(SARCASM_REGEX, json_dict['selftext']))
    is_serious = bool(re.search(SERIOUS_REGEX, json_dict['selftext']))

    # Filter posts out with no tone indicators
    if not is_sarcastic and not is_serious:
        global no_tone
        no_tone += 1
        return None
        # DEBUG
        # return json_dict

    # Increment stats
    if is_serious:
        global serious_count
        serious_count += 1
    if is_sarcastic:
        global sarcasm_count
        sarcasm_count += 1

    # Add labels to json dict so we don't have to re-parse posts later.
    json_dict['sarcastic'] = int(is_sarcastic)
    json_dict['serious'] = int(is_serious)
    return json_dict


def process_json_str(json_str: bytes) -> str | None:
    """Perform all the cleaning and classifying on a single string from the data file"""
    json_str = json_str.decode()
    json_str = json_str.strip()
    global bad_input_str
    if not json_str or json_str == '' or not json_str.startswith('{'):
        bad_input_str += 1
        return None

    json_dict: dict = json.loads(json_str)
    json_dict = validate_json(json_dict)
    if not json_dict:
        return None

    # Remove non-ascii chars and URLs from the post's selftext attribute.
    json_dict = clean_text(json_dict)
    if not json_dict:
        return None

    # Add labels to the json dict indicating if the text contains tone indicators. Drop the line if it doesn't.
    # json_dict = tone_indicator_filter_and_labeler(json_dict)
    #if not json_dict:
    #    pass
        # return None  # commented out for debugging

    # Serialize the json dict back into a string so we can write it to a file.
    return json.dumps(json_dict)


def main():
    # Read lines out of compressed dataset
    jsons = ZstdFile(DATA_FILE, 'r').readlines()
    total_posts = len(jsons)

    # Do all the cleaning & classification & labeling work in parallel; invalid entries are replaced by None
    jsons = Parallel(n_jobs=JOB_COUNT, prefer='threads')(
        delayed(process_json_str)(j) for j in jsons)

    # Filter out None values & make one big jsonl string to write to a file
    jsons = [j for j in jsons if j is not None]
    jsons = '\n'.join(jsons)

    # Write data to disk
    with open(OUTPUT_FILE, 'w') as f:
        f.write(jsons)

    # Print stats
    print(f'''Complete!
    
    Posts parsed from {DATA_FILE}:  {total_posts}
    Sarcastic posts:                         {sarcasm_count}
    Serious posts:                           {serious_count}
    
    Filtered, malformatted str: {bad_input_str}
    Fitlered, json validation: {validate_json_failed}
    Post deleted: {post_deleted}
    Post removed: {post_removed}
    Posts containing URLs: {contains_url}

    Percent sarcastic: {(sarcasm_count / total_posts) * 100}
    Percent serious:   {(serious_count / total_posts) * 100}

    ''')


if __name__ == '__main__':
    main()
