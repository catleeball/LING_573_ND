import re
import string
from datatrove.data import DocumentsPipeline, Document
from datatrove.executor import LocalPipelineExecutor
from datatrove.pipeline.base import PipelineStep
from datatrove.pipeline.filters.base_filter import BaseFilter
from datatrove.pipeline.readers import JsonlReader
from datatrove.pipeline.writers import JsonlWriter
from urlextract import URLExtract


INPUT_DIR = '/Volumes/media/Data/reddit/filtered_by_subreddit'
CLEANED_DIR = '/Volumes/media/Data/reddit/cleaned_data'
TONE_INDICATOR_DIR = '/Volumes/media/Data/reddit/tone_indicator_posts'
LOG_DIR = '/Volumes/media/Data/reddit/logs'
# URL_REGEX = re.compile(r"^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")
# URL_REGEX = re.compile(r'(http\S+)')
TONE_INDICATOR_REGEX = re.compile(r'(/s[\s$]|/sarcasm|/sarcastic|/serious|/srs)')

class RemoveNonASCII(PipelineStep):
    name = "Remove non-ASCII"

    def run(self, data: DocumentsPipeline, rank: int = 0, world_size: int = 1) -> DocumentsPipeline:
        for doc in data:
            with self.track_time():
                doc.text = str(filter(lambda c: c in string.printable, doc.text))
            yield doc


class RemoveURLs(PipelineStep):
    name = "Remove URLs"

    def run(self, data: DocumentsPipeline, rank: int = 0, world_size: int = 1) -> DocumentsPipeline:
        for doc in data:
            with self.track_time():
                url_extractor = URLExtract()
                # Get unique URLs in document text
                urls = set()
                for url in url_extractor.gen_urls(str(doc.text)):
                    urls.add(url)
                if urls:
                    self.stat_update("contains_url", value=doc.id)
                for url in urls:
                    doc.text.replace(url, '')
                # if 'http' in doc.text:
                #     self.stat_update("contains_url", value=doc.id)
                #     doc.text = re.sub(URL_REGEX, '', doc.text)
            yield doc


class ToneIndicatorFilter(BaseFilter):
    name = "Tone Indicator"

    def filter(self, doc: Document) -> bool:
        return bool(re.search(TONE_INDICATOR_REGEX, doc.text))


def clean():
    """Don't try to find tone indicators, just clean the data"""
    pipeline = [
        # Parse 'id' and 'selftext' attributes from each line Document objects
        JsonlReader(
            data_folder=INPUT_DIR,
            id_key='id',
            text_key='selftext',
        ),
        # Clean data in documents in-place
        RemoveNonASCII(),
        RemoveURLs(),
        JsonlWriter(
            output_folder=CLEANED_DIR,
            output_filename='data.gz',
            compression='gzip'
        )
    ]
    executor = LocalPipelineExecutor(
        pipeline=pipeline,
        logging_dir=LOG_DIR,
        workers=24,
    )
    executor.run()


def clean_and_classify():
    pipeline = [
        # Parse 'id' and 'selftext' attributes from each line Document objects
        JsonlReader(
            data_folder=INPUT_DIR,
            id_key='id',
            text_key='selftext',
        ),
        # Clean data in documents in-place
        RemoveNonASCII(),
        RemoveURLs(),
        # Keep only documents containing tone indicators
        ToneIndicatorFilter(),
        JsonlWriter(
            output_folder=CLEANED_DIR,
            output_filename='data.gz',
            compression='gzip'
        )
    ]
    executor = LocalPipelineExecutor(
        pipeline=pipeline,
        logging_dir=LOG_DIR,
    )
    executor.run()


if __name__ == '__main__':
    # clean()
    clean_and_classify()
