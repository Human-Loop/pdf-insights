from pathlib import Path
from typing import List, Optional

import pdfkit
import requests
from file_utils import lpa_exists
from fire import Fire
# from sec_edgar_downloader import Downloader
from distutils.spawn import find_executable
from tqdm.contrib.itertools import product

DEFAULT_OUTPUT_DIR = "data/"

DEFAULT_LPAS = [
    'Apax_Europe_VII_-_LPA_-_B_L.P_090323.pdf',
    'Advent_GPE_VI___LPA.pdf',
    'Cinven_V_LPA.pdf'
]

DEFAULT_FILE_TYPES = [
    "LPA",
]

def _download_file(
    lpa: str, file_type: str, output_dir: str, amount=None, before=None, after=None
):
    subdirectory = '/covenant-core-file-bucket-dev/us-east-1/files/'
    file_name = subdirectory + lpa  # Replace with your file name
    file_url ='https://covenant-core-file-bucket-dev.nyc3.digitaloceanspaces.com' + file_name
    # Initialize a session using DigitalOcean Spaces.
    download_path = output_dir  # Replace with the destination file path

    # Download the file
    response = requests.get(file_url)

    # Check if the download was successful
    if response.status_code == 200:
        with open(download_path + lpa, 'wb') as f:
            f.write(response.content)
        print(f"File has been downloaded to {download_path}")

    else:
        print(f"Failed to download the file. HTTP Status Code: {response.status_code}")

        print(f"{file_name} has been downloaded to {download_path}")


def _convert_to_pdf(output_dir: str):
    """Converts all html files in a directory to pdf files."""

    # NOTE: directory structure is assumed to be:
    # output_dir
    # ├── sec-edgar-filings
    # │   ├── AAPL
    # │   │   ├── 10-K
    # │   │   │   ├── 0000320193-20-000096
    # │   │   │   │   ├── filing-details.html
    # │   │   │   │   ├── filing-details.pdf   <-- this is what we want

    data_dir = Path(output_dir) / "sec-edgar-filings"
    for cik_dir in data_dir.iterdir():
        for filing_type_dir in cik_dir.iterdir():
            for filing_dir in filing_type_dir.iterdir():
                filing_doc = filing_dir / "filing-details.html"
                filing_pdf = filing_dir / "filing-details.pdf"
                if filing_doc.exists() and not filing_pdf.exists():
                    print("- Converting {}".format(filing_doc))
                    input_path = str(filing_doc.absolute())
                    output_path = str(filing_pdf.absolute())
                    try:
                        pdfkit.from_file(input_path, output_path, verbose=True)
                    except Exception as e:
                        print(f"Error converting {input_path} to {output_path}: {e}")

def main(
    output_dir: str = DEFAULT_OUTPUT_DIR,
    lpas: List[str] = DEFAULT_LPAS,
    file_types: List[str] = DEFAULT_FILE_TYPES,
    before: Optional[str] = None,
    after: Optional[str] = None,
    amount: Optional[int] = 3,
    convert_to_pdf: bool = False,
):
    print('Downloading filings to "{}"'.format(Path(output_dir).absolute()))
    print("File Types: {}".format(file_types))
    if convert_to_pdf:
        if find_executable("wkhtmltopdf") is None:
            raise Exception(
                "ERROR: wkhtmltopdf (https://wkhtmltopdf.org/) not found, "
                "please install it to convert html to pdf "
                "`sudo apt-get install wkhtmltopdf`"
            )
    for lpa, file_type in product(lpas, file_types):
        try:
            if lpa_exists(lpa, file_type, output_dir):
                print(f"- File for {symbol} {file_type} already exists, skipping")
            else:
                print(f"- Downloading file for {lpa} {file_type}")
                _download_file(lpa, file_type, output_dir, amount, before, after)
        except Exception as e:
            print(
                f"Error downloading lpa={lpa} & file_type={file_type}: {e}"
            )

    if convert_to_pdf:
        print("Converting html files to pdf files")
        _convert_to_pdf(output_dir)


if __name__ == "__main__":
    Fire(main)