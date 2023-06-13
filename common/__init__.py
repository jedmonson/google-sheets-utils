import argparse
import codecs
import json
import os

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

parser = argparse.ArgumentParser(
    add_help=False, description="Common utilities for working with google sheet data."
)

parser.add_argument("sheet_key", help="The google sheet ID to push/pull to/from.")

parser.add_argument(
    "worksheet_name", help="The name of the worksheet to push/pull to/from."
)

parser.add_argument(
    "--format",
    help="Output format type. [csv, json, jsonlines]",
    dest="output_format",
    default="jsonlines",
)

parser.add_argument(
    "files",
    metavar="FILE",
    nargs="*",
    help="Files to read into google sheets. (If empty, stdin is used)",
)

args = parser.parse_args()

gc = gspread.authorize(
    Credentials.from_service_account_info(
        json.loads(
            codecs.decode(os.environ["GOOGLE_SHEET_CREDS"].encode(), "base64").decode()
        ),
        scopes=[
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ],
    )
)
