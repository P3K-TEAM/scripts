import ijson
from pathlib import Path
from dotenv import load_dotenv
from os import getenv
from elasticsearch import Elasticsearch, helpers

ROOT_DIR = Path(__file__).resolve().parents[3]

# load .env file
load_dotenv()

# elasticsearch python client
es = Elasticsearch(
    getenv("ELASTIC_HOST"),
    http_auth=(getenv("ELASTIC_USER"), getenv("ELASTIC_PASSWORD")),
    port=getenv("ELASTIC_PORT"),
)
es_index_name = getenv("ELASTIC_INDEX_NAME")


# method for bulk index
def bulk_index(elastic, data, index):
    try:
        actions = [
            {
                "_index": index,
                "_source": item
            } for item in data
        ]
        helpers.bulk(elastic, actions)
    except Exception as e:
        print("ERROR:", e)


# source file preparation
source_file = open(ROOT_DIR.joinpath('data/wikipedia.json'), encoding="utf-8")

# bulk list to store items
BULK_SIZE = 1000
data = []

# reading json in streams
file_items = ijson.items(source_file, 'item')
for item in file_items:

    # rename fields to match elastic index mapping
    data.append({
        'language': item['language'],
        'name': item['title'],
        'text_raw': item['raw_text'],
        'source': 'wikipedia.sk'
    })

    # if the bulk reaches the limit, bulk index the data
    if len(data) >= BULK_SIZE:
        bulk_index(es, data, es_index_name)
        data.clear()

# bulk index remaining data
if len(data):
    bulk_index(es, data, es_index_name)
