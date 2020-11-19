##Crawler for referaty.centrum.sk
Crawler use using [Scrapy](https://scrapy.org) framework for python. 

### Prerequisites
 - Python ^3.0
 - [Anaconda](https://www.anaconda.com/products/individual) 
 
## Installation 

1. Open Anaconda Prompt where `requirements.yml` is
1. Create new env for Scrapy crawler with all dependencies

    ```
    conda env create -f requirements.yml
    ```


##Usage
 
1. Activate the conda environment 
    ```
    conda activate scrapy
    ```

1. Use this command in scrapy environment to run crawler:

    ```
    scrapy runspider scraper.py
    ```




