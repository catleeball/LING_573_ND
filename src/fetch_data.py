from datetime import datetime
from pathlib import Path
import requests


# relative paths assume you're running from the root of the repo, e.g. "python src/sarc.py"
DOWNLOAD_DIR = 'data/sarc'
SARC_URL_FILE = Path('data/sarc/sarc_urls.csv')


def get_sarc_urls(
        sarc_url_file: str = SARC_URL_FILE
) -> dict[str, tuple[str, str]]:
    """Read SARC data URLs from file, return a dict of {url, (filename, sarc_dir)}."""
    sarc_urls = {}
    with open(sarc_url_file) as f:
        for line in f:
            if not line:
                pass
            line = line.strip()
            url, sarc_dir, filename = line.split(sep=',', maxsplit=3)
            sarc_urls[url] = (filename, sarc_dir)

    if not sarc_urls:
        raise ValueError(f'No URLs parsed from {sarc_url_file}')

    return sarc_urls


def download_sarc_data(
        overwrite_local_files: bool = False
):
    """Check if we have sarc data locally. If not, download it."""
    if not Path(DOWNLOAD_DIR).exists():
        raise ValueError(f"Can't find data dir: `{DOWNLOAD_DIR}`. Are you running this from the root of the repository? E.g. `python src/fetch_data.py` from `./LING_573_ND`")

    url_dict = get_sarc_urls()

    for url, file_tuple in url_dict.items():
        filename, sarc_dir = file_tuple
        local_path = Path(f'{DOWNLOAD_DIR}/{sarc_dir.strip()}/{filename.strip()}')

        if not local_path.exists() or overwrite_local_files:
            print(f'[{datetime.now()}] DEBUG: Downloading {local_path}')
            download_file(url, local_path)
            print(f'[{datetime.now()}] DEBUG: Download complete!')
        else:
            print(f'[{datetime.now()}] DEBUG: {local_path} exists already. Not downloading.')


def download_file(
        url: str,
        local_path: Path
):
        response = requests.get(url, stream=True)

        if not response.ok:
            raise requests.HTTPError(f'Failed to download url: `{url}`. HTTP status code: {response.status_code}')

        with open(local_path, 'wb') as f:
            f.write(response.content)


if __name__ == '__main__':
    # If we're running fetch_data.py as a script, just ensure that we have the datasets locally
    download_sarc_data()
