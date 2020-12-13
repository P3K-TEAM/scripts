## Imports

This script imports the data crawled by crawlers in this repository

### Prerequisites

- Python ^3.0
- [Pipenv](https://pypi.org/project/pipenv/)
- Running [ElasticSearch](https://elastic.co) instance with index created

## Installation

1. Install all dependencies

    ```
    pipenv install
    ```

## Usage

1. Fill in the credentials to ElasticSearch datastore such as port, hostname into `.env` file. \
   If you do not use ElasticSearch authorization leave the files empty.
    ```
   ELASTIC_HOST=localhost
   ELASTIC_PORT=9200
   ELASTIC_USER=user
   ELASTIC_PASSWORD=secret
   ELASTIC_INDEX_NAME=documents
   DEBUG=true
   SOURCE_FILE_PATH=data/referaty.json
   FIELD_MAP={ "language": "language", "name": "title", "access_url": "url" }
   ADDITIONAL_FIELDS={ "source": "referaty.sk" }
   BULK_SIZE=300
    ```  

1. Use this command in pipenv environment to run the import:
    ```
    pipenv run python script.py
    ```




