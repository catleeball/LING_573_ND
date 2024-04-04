from datetime import datetime
import sys
from enum import Enum
from functools import cached_property
import re
import praw
from praw.models import Comment, Submission
# Note that secrets.py is in the .gitignore; it's just a file with the constants we import here set
from secrets import CLIENT_ID, CLIENT_SECRET


# Max posts to fetch; low value for testing
POST_LIMIT = 100


# User agent format suggested here: https://praw.readthedocs.io/en/stable/getting_started/quick_start.html#prerequisites
USER_AGENT = 'macos:tone_indicator_scraper:v0.1 (by u/__eel__)'

KNOWN_TAG_REGEX = re.compile(
    pattern=r'([/\\]sarcasm[.\s\n?!)]|[/\\]sarc[.\s\n?!)]|[/\\]s[.\s\n?!)]|[/\\]srs[.\s\n?!)]|[/\\]serious[.\s\n?!)])',
    flags=re.MULTILINE,
)
# This is probably super prone to false positives
ALL_TAG_REGEX = re.compile(
    pattern=r'([/\\]\w*[.\s\n?!)])',
    flags=re.MULTILINE,
)
SARCASM_TAGS = {'/s', '/sarc', '/sarcasm', '/sarcastic', r'\s', r'\sarc', r'\sarcasm', r'\sarcastic'}
SERIOUS_TAGS = {'/srs', '/serious', r'\srs', r'\serious'}
ALL_KNOWN_TAGS = {'/s', '/sarc', '/sarcasm', '/sarcastic', r'\s', r'\sarc', r'\sarcasm', r'\sarcastic', '/srs', '/serious', r'\srs', r'\serious'}


class TextType(Enum):
    """Whether this text sample came from a Reddit submission or comment."""
    submission = True
    comment    = False

    @staticmethod
    def from_post(post: Comment | Submission) -> 'TextType':
        """Constructor which infers TextType's value from the object's type"""
        if isinstance(post, Comment):
            return TextType.submission
        if isinstance(post, Submission):
            return TextType.comment
        raise ValueError(f'Argument `post` has type `{type(post)}`. '
                         'Expected one of: praw.models.Submission, praw.models.Comment')


def get_post_text(post: Comment | Submission) -> str:
    if isinstance(post, Comment):
        # Add a trailing space to prop up my bad regexes :lolsob:
        return f'{post.body} '
    if isinstance(post, Submission):
        # Submissions have both title and body text; concatenate them for tag detection.
        return f'{post.title} {post.selftext} '


class TextSample:
    """Container for relevant data about a reddit submission or comment. Note the cached properties for lazy parsing."""
    id:        str
    text_type: TextType
    text:      str

    def __init__(self, post: Comment | Submission):
        self.id        = post.id
        self.text_type = TextType.from_post(post)
        self.text      = get_post_text(post)

    @cached_property
    def is_sarcastic(self) -> bool:
        return bool(len(self.sarcastic_tags))

    @cached_property
    def is_serious(self) -> bool:
        return bool(len(self.serious_tags))

    @cached_property
    def tags(self) -> list[str]:
        """Returns all tags detected in this sample. May contain duplicates. Uses KNOWN_TAG_REGEX for only specified tags."""
        # Most posts don't have tone indicators, and checking for '/' is faster than running the regex, so do this first
        if '/' not in self.text and '\\' not in self.text:
            return []

        known_tags = []
        for match in re.finditer(pattern=KNOWN_TAG_REGEX, string=self.text):
            for match_group in match.groups():
                known_tags.append(match_group.strip())

        return known_tags

    @cached_property
    def sarcastic_tags(self) -> list[str]:
        """Returns all tags in this sample that denote sarcasm including duplicates. (e.g. ['/s', '/s', '/sarcastic'])"""
        return [tag for tag in self.tags
                if tag in SARCASM_TAGS]

    @cached_property
    def serious_tags(self) -> list[str]:
        """Returns all tags in this sample that denote seriousness including duplicates. (e.g. ['/srs', '/srs', '/serious'])"""
        return [tag for tag in self.tags
                if tag in SERIOUS_TAGS]

    @cached_property
    def all_possible_tags(self) -> list[str]:
        """Returns all tokens that look like tags. May contain duplicates."""
        if '/' not in self.text and '\\' not in self.text:
            return []

        all_tags = []
        for match in re.finditer(pattern=KNOWN_TAG_REGEX, string=self.text):
            for match_group in match.groups():
                all_tags.append(match_group.strip())

        return all_tags

    @cached_property
    def unknown_tags(self) -> list[str]:
        """All tokens that look like tags and aren't ones we know to look for."""
        return [tag for tag in self.all_possible_tags
                if tag not in ALL_KNOWN_TAGS]

    def __eq__(self, other) -> bool:
        if not isinstance(other, TextSample):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id + self.text)


def read_only_reddit_client() -> praw.Reddit:
    # add params username='' and password='' to get an RW client
    return praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
    )


def scrape_subreddit(
        reddit_client: praw.Reddit,
        subreddit_name: str,
        post_limit: int | None,
) -> list[TextSample]:
    """Fetch up to `post_limit` submissions and their comments from `subreddit_name`."""
    # TODO: query posts older than given datetime to allow iteratively building dataset
    #
    # Jargon note: 'Submissions' are a reddit post, and 'Comments' are replies to the post. See the praw model doc:
    #     - https://praw.readthedocs.io/en/stable/code_overview/praw_models.html
    #
    # Additional refs:
    #    submission extraction: https://praw.readthedocs.io/en/stable/getting_started/quick_start.html#obtain-submission-instances-from-a-subreddit
    #    comment extraction: https://praw.readthedocs.io/en/stable/tutorials/comments.html

    samples: list[TextSample] = []

    # Iterate submissions and their comments
    for submission in reddit_client.subreddit(subreddit_name).new(limit=post_limit):
        submission: Submission
        samples.append(TextSample(submission))
        for comment in submission.comments.list():
            samples.append(TextSample(comment))

    return samples


def analyze_samples(samples: list[TextSample], subreddits_sampled: str) -> str:
    """Gather stats about the samples gathered."""
    sample_count: int = len(samples)
    samples = set(samples)
    unique_sample_count: int = len(samples)
    duplicate_sample_count: int = sample_count - unique_sample_count

    if duplicate_sample_count > 0:
        sys.stderr.write(f'WARNING: Duplicate samples. Raw sample count: {sample_count}; Unique sample count: {unique_sample_count}\n')

    submission_count:                    int = 0
    comment_count:                       int = 0
    total_tag_count:                     int = 0
    total_known_tag_count:               int = 0
    total_unknown_tag_count:             int = 0
    samples_with_sarcasm_count:          int = 0
    samples_with_serious_count:          int = 0
    samples_with_unknown_tags_count:     int = 0
    samples_with_no_known_tags_count:    int = 0
    samples_with_no_possible_tags_count: int = 0
    samples_with_known_tags_count:       int = 0
    samples_with_no_unknown_tags_count:  int = 0
    samples_with_possible_tags_count:    int = 0

    known_tags_seen:   set[str] = set()
    unknown_tags_seen: set[str] = set()

    for sample in samples:
        match sample.text_type:
            case TextType.submission:
                submission_count += 1
            case TextType.comment:
                comment_count += 1

        known_tags_seen.update(set(sample.tags))
        unknown_tags_seen.update(set(sample.unknown_tags))

        samples_with_sarcasm_count += int(sample.is_sarcastic)
        samples_with_serious_count += int(sample.is_serious)

        all_tag_count = len(sample.all_possible_tags)
        known_tag_count = len(sample.tags)
        unk_tag_count = len(sample.unknown_tags)

        total_tag_count += all_tag_count
        total_known_tag_count += known_tag_count
        total_unknown_tag_count += unk_tag_count

        if all_tag_count == 0:
            samples_with_no_possible_tags_count += 1
        else:
            samples_with_possible_tags_count += 1

        if known_tag_count == 0:
            samples_with_no_known_tags_count += 1
        else:
            samples_with_known_tags_count += 1

        if unk_tag_count == 0:
            samples_with_no_unknown_tags_count += 1
        else:
            samples_with_unknown_tags_count += 1

    known_tags_unseen = ALL_KNOWN_TAGS - known_tags_seen
    known_tags_unseen_str = ', '.join(known_tags_unseen)
    unknown_tags_seen_str = ', '.join(unknown_tags_seen)

    rate_of_posts_containing_sarcasm_tags: float = (samples_with_sarcasm_count / unique_sample_count) * 100
    rate_of_posts_containing_serious_tags: float = (samples_with_serious_count / unique_sample_count) * 100
    rate_of_posts_containing_known_tags:   float = (samples_with_known_tags_count / unique_sample_count) * 100
    rate_of_posts_containing_tags:         float = (samples_with_possible_tags_count / unique_sample_count) * 100
    rate_of_posts_with_no_known_tags:      float = (samples_with_no_known_tags_count / unique_sample_count) * 100
    rate_of_posts_with_no_detected_tags:   float = (samples_with_no_possible_tags_count / unique_sample_count) * 100

    return f'''[{datetime.now()}]
-----  Analysis of {POST_LIMIT} submissions for each subreddit(s): {subreddits_sampled}  -----

unique_sample_count:                 {unique_sample_count}
duplicate_sample_count:              {duplicate_sample_count}
submission_count:                    {submission_count}
comment_count:                       {comment_count}

total_tag_count:                     {total_tag_count}
total_known_tag_count:               {total_known_tag_count}
total_unknown_tag_count:             {total_unknown_tag_count}

samples_with_sarcasm_count:          {samples_with_sarcasm_count}
samples_with_serious_count:          {samples_with_serious_count}
samples_with_unknown_tags_count:     {samples_with_unknown_tags_count}
samples_with_no_known_tags_count:    {samples_with_no_known_tags_count}
samples_with_no_possible_tags_count: {samples_with_no_possible_tags_count}

Known tags which were not observed:  {known_tags_unseen_str}
Unknown tags observed:               {unknown_tags_seen_str}

rate_of_posts_containing_serious_tags:  {rate_of_posts_containing_serious_tags}%
rate_of_posts_containing_known_tags:    {rate_of_posts_containing_known_tags}%
rate_of_posts_containing_sarcasm_tags:  {rate_of_posts_containing_sarcasm_tags}%
rate_of_posts_containing_tags:          {rate_of_posts_containing_tags}%
rate_of_posts_with_no_known_tags:       {rate_of_posts_with_no_known_tags}%
rate_of_posts_with_no_detected_tags:    {rate_of_posts_with_no_detected_tags}%

'''


def main():
    # TODO: use config file / cli flags / env vars for configurations rather than lots of constants
    # TODO: add unit tests
    print(f'DEBUG [{datetime.now()}]: Starting...')

    reddit_client = read_only_reddit_client()
    subreddits = ('neurodivergent', )

    print(f'DEBUG [{datetime.now()}]: Got client. Fetching posts...')

    sample_sets: list[list[TextSample]] = []

    for sub in subreddits:
        sample_sets.append(
            scrape_subreddit(
                reddit_client=reddit_client,
                subreddit_name=sub,
                post_limit=POST_LIMIT))

    print(f'DEBUG [{datetime.now()}]: Got posts. Parsing and analyzing...')

    subreddits_str = ', '.join(subreddits)

    for sample_set in sample_sets:
        analysis = analyze_samples(sample_set, subreddits_str)
        print(analysis)
        with open('scrape_log.txt', 'w') as f:
            f.write(analysis)

    print(f'DEBUG [{datetime.now()}]: Done!')


if __name__ == '__main__':
    main()
