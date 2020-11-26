## Import Referaty.sk
This script imports the data crawled by the crawler [included in this repository](https://github.com/P3K-TEAM/scripts/tree/master/src/crawler_referaty). 

### Prerequisites
 - Python ^3.0
 - [Pipenv](https://pypi.org/project/pipenv/)
 - Running [ElasticSearch](https://elastic.co) instance with `documents` created 
 
## Installation 

1. Install all dependencies  

    ```
    pipenv install
    ```

## Usage
 
1. Activate the pipenv environment 
    ```
    pipenv shell
    ```

1. Fill in the credentials to ElasticSearch datastore such as port, hostname into `.env` file. \
 If you do not use ElasticSearch authorization leave the files empty.
    ```
    ELASTIC_HOST=localhost
    ELASTIC_PORT=9200
    ELASTIC_USER=
    ELASTIC_PASSWORD=
    ELASTIC_INDEX_NAME=documents
    ```  

1. Use this command in pipenv environment to run the import:
    ```
    python script.py
    ```




