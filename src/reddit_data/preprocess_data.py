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
LOG_DIR = '/Media/Data/reddit/.logs'
# URL_REGEX = re.compile(r"^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")
URL_REGEX = re.compile(r'''
['"(]*http[\S)'"$]+
''')
# TONE_INDICATOR_REGEX = re.compile(r'([^\S]/s[\S$]|[^\S]/sarcasm[\S$]|[^\S]/sarcastic[\S$]|[^\S]/serious[\S$]|[^\S]/srs[\S$])')
SARCASM_INDICATOR_REGEX = re.compile(r'([^\s]?[/\\]s[\S$.,?!]?|[^\s]?[/\\]sarcasm[\S$.,?!]?|[^\s]?[/\\]sarcastic[\S$.,?!]?)')
SERIOUS_INDICATOR_REGEX = re.compile(r'([^\s]?[/\\]serious[\S$.,?!]?|[^\s]?[/\\]srs[\S$.,?!]?)')

BAD_ID = 'BAD'
BAD_JSON = {'text': '', 'id': BAD_ID, 'metadata': {}}

ALLOWED_CHARS = string.ascii_letters + string.digits + string.whitespace + r"""
" ',.?!/
"""

class RemoveNonASCII(PipelineStep):
    name = 'Remove non-ASCII'
    type = 'Transformer'

    def run(self, data: DocumentsPipeline, rank: int = 0, word_size: int = 1) -> DocumentsPipeline:
        for doc in data:
            with self.track_time():
                # string.printable left characters in that later broke json serialization :(
                doc.text = ''.join([c for c in doc.text if c in ALLOWED_CHARS])
                for val in doc.metadata.values():
                    doc.text = ''.join([c for c in doc.text if c in ALLOWED_CHARS])
            yield doc


class RemoveURLs(PipelineStep):
    name = 'Remove URLs'
    type = 'Transformer'

    def run(self, data: DocumentsPipeline, rank: int = 0, word_size: int = 1) -> DocumentsPipeline:
        for doc in data:
            with self.track_time():
                if 'http' in doc.text:
                    self.stat_update("contains_url")
                    doc.text = re.sub(URL_REGEX, '', doc.text)
            yield doc


class ToneIndicatorLabeler(PipelineStep):
    name = 'Tone Indicator'
    type = 'Transformer'

    def run(self, data: DocumentsPipeline, rank: int = 0, word_size: int = 1) -> DocumentsPipeline:
        for doc in data:
            with self.track_time():
                sarcastic = bool(re.search(SARCASM_INDICATOR_REGEX, doc.text))
                serious = bool(re.search(SERIOUS_INDICATOR_REGEX, doc.text))
                self.stat_update("sarcastic")
                self.stat_update("serious")
                doc.metadata['sarcastic'] = int(sarcastic)
                doc.metadata['serious'] = int(serious)
            yield doc


class EmptyPostFilter(BaseFilter):
    name = 'Filter Empty Posts'

    def filter(self, doc: Document) -> bool | Tuple[bool, str]:
        if doc.id == BAD_ID:
            yield False
        # We only want text long enough to fit a tone indicator
        match doc.text.strip():
            case None | '' | '[deleted]' | '[removed]':
                yield False
            case _:
                yield True


def jsonl_text_extraction_adapter(data: dict, path: str, id_in_file: int | str) -> dict:
    # Comment objects have the `body` attribute
    if 'body' in data:
        text_key = data.pop('body')
    elif 'selftext' in data:
        text_key = data.pop('selftext')
    else:
        return BAD_JSON
    return {
        'text': text_key,
        'id': data.pop('id', f'{path}/{id_in_file}'),
        # "metadata": data.pop("metadata", {}) | data,  # remaining data goes into metadata
        'metadata': {
            'author': data.get('author', ''),
            'title': data.get('title', ''),
            'subreddit': data.get('subreddit', ''),
            'subreddit_id': data.get('subreddit_id', ''),
            'permalink': data.get('permalink', ''),
            'created_utc': str(data.get('created_utc', '')),
        }
    }


def clean_and_classify():
    pipeline = [
        # Parse 'id' and 'selftext'/'body' attributes from each line Document objects
        JsonlReader(
            data_folder=INPUT_DIR,
            adapter=jsonl_text_extraction_adapter,
        ),
        # Remove empty / invalid posts
        EmptyPostFilter(),
        # Clean data in documents in-place
        RemoveNonASCII(),
        RemoveURLs(),
        # Write all cleaned data before proceeding to tone classification.
        JsonlWriter(
            output_folder=CLEANED_DIR,
            output_filename='data.gz',
            compression='gzip'
        ),
        # Tag metadata section of docs with whether they do or don't contain tone.
        ToneIndicatorLabeler(),
        # Write data containing tone indicators
        JsonlWriter(
            output_folder=TONE_INDICATOR_DIR,
            output_filename='data.gz',
            compression='gzip'
        )
    ]
    executor = LocalPipelineExecutor(
        pipeline=pipeline,
        logging_dir=LOG_DIR,
        tasks=24,
        workers=-1,
    )
    executor.run()


if __name__ == '__main__':
    clean_and_classify()
