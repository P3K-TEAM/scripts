## Process SK wikipedia dump

### Prerequisites
 - Python ^3.0
 - [Pipenv](https://pypi.org/project/pipenv/)
 
  
## Installation 

1. Install all dependencies  

    ```
    pipenv install
    ```

## Usage
1. Download [wikipedia dump](https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/skwiki/20201101/skwiki-20201101-pages-articles.xml.bz2)

1. Activate the pipenv environment     
   ```
    pipenv shell
    ```

 1. XML file is too large - you need to parse it into smaller pieces using `xml_breaker.py` 
    ```
    python xml_breaker.py
    ```

1. Run the script
   ```
   python wikipedia_dump.py
   ```


