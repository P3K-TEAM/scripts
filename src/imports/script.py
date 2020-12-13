import ijson
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from os import getenv

from helpers.logging import Logging
from helpers.make_request import make_request
from config.connection import Connection

# Load .env file
load_dotenv()

# Settings
ROOT_DIR = Path(__file__).resolve().parents[2]

DEBUG = getenv("DEBUG")

logging = Logging(datetime.now(), DEBUG)

connection = Connection(
    hostname=getenv("ELASTIC_HOST"),
    port=getenv("ELASTIC_PORT"),
    index=getenv("ELASTIC_INDEX_NAME"),
)

auth = requests.auth.HTTPBasicAuth(getenv("ELASTIC_USER"), getenv("ELASTIC_PASSWORD"))

source_file = open(ROOT_DIR.joinpath(getenv("SOURCE_FILE_PATH")), encoding="utf-8")

mapping = json.loads(getenv('FIELD_MAP'))
additional_fields = json.loads(getenv('ADDITIONAL_FIELDS'))


def bulk_index(data):
    """
    Method for bulk index
    :param data: data to be indexed
    :return:
    """

    def bulk_api_string(item):
        return f"{{\"index\":{{}}\n{json.dumps(item)}"

    body = '\n'.join([bulk_api_string(item) for item in data]) + '\n'

    return make_request(
        requests.post,
        url=f"{connection.hostname}:{connection.port}/{connection.index}/_bulk",
        headers={'Content-Type': 'application/json'},
        auth=auth,
        data=body
    )


def start_import(bulk_size):
    # Bulk list to store items
    data = []
    total_uploaded = 0

    # Reading json in streams
    file_items = ijson.items(source_file, 'item')
    for item in file_items:

        # Rename fields to match elastic index mapping
        data.append({
            **{key_to: item[key_from] for key_to, key_from in mapping.items()},
            **additional_fields
        })

        # If the bulk reaches the limit, bulk index the data
        if len(data) >= bulk_size:
            bulk_index(data)
            total_uploaded += len(data)
            logging.log(f'Total indexed items: {total_uploaded}')
            data.clear()

    # Index the remaining data
    if len(data):
        bulk_index(data)

    logging.log("Import finished.")

# Run the import
start_import(int(getenv('BULK_SIZE')))
