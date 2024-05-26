import re
import string
from typing import Tuple
from datatrove.data import DocumentsPipeline, Document
from datatrove.executor import LocalPipelineExecutor
from datatrove.pipeline.base import PipelineStep
from datatrove.pipeline.filters.base_filter import BaseFilter
from datatrove.pipeline.readers import JsonlReader
from datatrove.pipeline.writers import JsonlWriter

INPUT_DIR = '/Media/Data/reddit/Selected_Subreddits_Data_Small_Chunked_Files_Compressed'
CLEANED_DIR = '/Media/Data/reddit/Cleaned_Data'
TONE_INDICATOR_DIR = '/Media/Data/reddit/Tone_Indicator_Data'
LOG_DIR = '/Media/Data/reddit/logs2'
# URL_REGEX = re.compile(r"^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")
URL_REGEX = re.compile(r'''
['"(]*http[\S)'"$]+
''')
# TONE_INDICATOR_REGEX = re.compile(r'([^\S]/s[\S$]|[^\S]/sarcasm[\S$]|[^\S]/sarcastic[\S$]|[^\S]/serious[\S$]|[^\S]/srs[\S$])')
SARCASM_INDICATOR_REGEX = re.compile(r'([^\s]?[/\\]s[\s$.,?!]?|[^\s]?[/\\]sarcasm[\s$.,?!]?|[^\s]?[/\\]sarcastic[\s$.,?!]?)')
SERIOUS_INDICATOR_REGEX = re.compile(r'([^\s]?[/\\]serious[\s$.,?!]?|[^\s]?[/\\]srs[\s$.,?!]?)')

BAD_ID = 'BAD'
BAD_JSON = {'text': '', 'id': BAD_ID, 'metadata': {}}

ALLOWED_CHARS = string.ascii_letters + string.digits + r"""
.?! /
"""


def clean_str(s: str) -> str:
    if not s or s == '':
        return ''
    buffer = []
    for c in s:
        if c == '\\':
            buffer.append('/')
            continue
        if c in string.whitespace:
            buffer.append(' ')
            continue
        if c in ALLOWED_CHARS:
            buffer.append(c)
            continue

    return ''.join(buffer)


class ToneIndicatorLabeler(PipelineStep):
    name = 'Tone Indicator Labeler'
    type = 'Transformer'

    def run(self, data: DocumentsPipeline, rank: int = 0, word_size: int = 1) -> DocumentsPipeline:
        for doc in data:
            with self.track_time():
                sarcastic = bool(re.search(SARCASM_INDICATOR_REGEX, doc.text))
                serious = bool(re.search(SERIOUS_INDICATOR_REGEX, doc.text))
                self.stat_update("sarcastic", int(sarcastic))
                self.stat_update("serious", int(serious))
                doc.metadata['sarcastic'] = int(sarcastic)
                doc.metadata['serious'] = int(serious)
            yield doc


class EmptyPostFilter(BaseFilter):
    name = 'Filter Empty Posts'

    def filter(self, doc: Document) -> bool | Tuple[bool, str]:
        if doc.id == BAD_ID:
            yield False
        match doc.text.strip():
            case None | '' | '[deleted]' | '[removed]':
                yield False
            case _:
                yield True


# class SubredditFilter(BaseFilter):
#     name = 'Filter to only ND subreddits'
#     subreddits = ('adhd', 'adhdwomen', 'aspergirls', 'autismtranslated', 'autismmemes', 'autisticpride', 'autism',
#                   'autisticadults', 'autisminwomen', 'neurodivergent', 'neurodivergentlbgtq',)
#
#     def filter(self, doc: Document) -> bool | Tuple[bool, str]:
#         if doc.metadata['subreddit'].lower() in self.subreddits:
#             yield True
#         else:
#             yield False


def jsonl_text_extraction_adapter(data: dict, path: str, id_in_file: int | str) -> dict:
    # Comment objects have the `body` attribute; Submission objects have 'selftext'
    if 'body' in data:
        text_key = clean_str(data.pop('body'))
    elif 'selftext' in data:
        text_key = clean_str(data.pop('selftext'))
    else:
        return BAD_JSON

    # ensure all data has only allowed chars
    author = clean_str(data.get('author', ''))
    title = clean_str(data.get('title', ''))
    subreddit = clean_str(data.get('subreddit', ''))
    subreddit_id = clean_str(data.get('subreddit_id', ''))
    created_utc = clean_str(str(data.get('created_utc', '')))

    # Remove URLs
    if 'http' in text_key:
        text_key = re.sub(URL_REGEX, '', text_key)

    if not text_key:
        return BAD_JSON

    return {
        'text': text_key,
        'id': clean_str(data.pop('id', f'{path}/{id_in_file}')),
        'metadata': {
            'author': author,
            'title': title,
            'subreddit': subreddit,
            'subreddit_id': subreddit_id,
            'created_utc': created_utc,
        },
    }


def jsonl_writer_adapter(doc: Document) -> dict:
    return {
        'id': doc.id,
        'text': doc.text,
        'author': doc.metadata['author'],
        'title': doc.metadata['title'],
        'subreddit': doc.metadata['subreddit'],
        'subreddit_id': doc.metadata['subreddit_id'],
        'created_utc': doc.metadata['created_utc'],
        'sarcastic': doc.metadata['sarcastic'],
        'serious': doc.metadata['serious'],
    }


def clean_and_classify():
    pipeline = [
        # Parse 'id' and 'selftext'/'body' attributes from each line Document objects
        # Same as JsonlReader, but each line is run through clean_str() before being made into a Document
        JsonlReader(
            data_folder=INPUT_DIR,
            adapter=jsonl_text_extraction_adapter,
        ),
        # Remove empty / invalid posts
        EmptyPostFilter(),
        # Tag metadata section of docs with whether they do or don't contain tone.
        ToneIndicatorLabeler(),
        # Write data containing tone indicators. Same as JsonlWriter, but
        # we set ensure_ascii=True, use minimal separators, and we assert the serialized strings can be deserialized
        JsonlWriter(
            output_folder=TONE_INDICATOR_DIR,
            output_filename='regex_retry_data.jsonl',
            compression=None,
            adapter=jsonl_writer_adapter
        )
    ]
    executor = LocalPipelineExecutor(
        pipeline=pipeline,
        logging_dir=LOG_DIR,
    )
    executor.run()


if __name__ == '__main__':
    clean_and_classify()
