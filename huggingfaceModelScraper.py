# Import libraries

import argparse
import logging
import json
import numpy as np
import pandas as pd
import requests
import time

from bs4 import BeautifulSoup
from datetime import timedelta


def get_model_urls(pages: int, headers: dict, sleep_time: int):
    """
    This function creates a list with all the model urls in
    'https://huggingface.co/models'

    :pages: number of pages to limit the scraping scope
    :headers: custom headers used in the GET requests
    """
    hf_url = 'https://huggingface.co'
    page = 0
    model_urls = []

    start_time = time.time()

    while True:
        hf_models_url = hf_url + f'/models?p={page}&sort=downloads'
        models_page = requests.get(hf_models_url, headers=headers)
        models_soup = BeautifulSoup(models_page.content, 'html.parser')
        model_boxes = models_soup.findAll('a', class_='block p-2')
        if len(model_boxes) == 0 or page > pages:
            break
        logging.info(f"Reading page: {page}")
        # do this for each page
        for model_box in model_boxes:
            model_url = hf_url + model_box.attrs['href']
            model_urls.append(model_url)
        page += 1
        # Sleep x seconds between requests
        time.sleep(sleep_time)

    end_time = time.time()
    logging.info(f"Number of model urls stored: {len(model_urls)}")
    logging.info(f"Elapsed time:  {timedelta(seconds=end_time - start_time)}")

    return model_urls


def get_model_attributes(url: str, headers: dict):
    """
    This funciton will get the attributes of each model registered
    in https://huggingface.co/models given the model URL.

    :url: url of an specific model
    :headers: custom headers used in the GET requests
    """
    model_page = requests.get(url, headers=headers)
    model_soup = BeautifulSoup(model_page.content, 'html.parser')
    fields = {}

    # get author, model name and likes
    likeButton = model_soup.find('div', attrs={'data-target': 'LikeButton'})
    if likeButton is None:
        logging.error(f'Error in likebutton: {url}')
    else:
        data_props = json.loads(likeButton.attrs['data-props'])
        repoId = data_props['repoId']
        repoId_split = repoId.split('/')
        # some models have an "explicit" author, others don't
        if len(repoId_split) == 1:
            fields['author'] = np.nan
            fields['model_name'] = repoId_split[0]
        else:
            fields['author'] = repoId_split[0]
            fields['model_name'] = repoId_split[1]

        fields['likes'] = data_props['likes']

    # get model attributes
    modelHeaderTags = model_soup.find('div', attrs={'data-target': 'ModelHeaderTags'})
    if modelHeaderTags is None:
        logging.error(f'Error in modelHeaderTags: {url}')
    else:
        data_props_str = modelHeaderTags.attrs['data-props']

        tagObjs = json.loads(data_props_str)['tagObjs']
        for tagObj in tagObjs:
            if not tagObj['type'] in fields:
                fields[tagObj['type']] = []
            fields[tagObj['type']].append(tagObj['id'])
            if tagObj['type'] == 'pipeline_tag':
                fields['subType'] = tagObj['subType']

    return fields


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--pages",
                        type=int,
                        help="Specify the number of pages you want to scrap.",
                        default=0,
                        required=False)
    parser.add_argument("-s", "--sleep",
                        type=int,
                        help="Specify the number seconds between requests.",
                        default=0,
                        required=False)
    arguments = parser.parse_args()

    # Initialize log
    log = logging.getLogger(__name__)  # This means that logger names track the package/module hierarchy
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info("Starting webscraping of https://huggingface.co/models")

    # Define custom headers
    custom_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    # Get the urls for all models in the given pages
    model_urls = get_model_urls(arguments.pages, custom_headers, arguments.sleep)

    # Convert scrapped data to a pandas dataframe
    start_time = time.time()

    df = pd.DataFrame()
    for url in model_urls:
        df = df.append(get_model_attributes(url, custom_headers), ignore_index=True)
        time.sleep(arguments.sleep)

    end_time = time.time()

    logging.info(f"Number of rows: {df.shape[0]}")
    logging.info(f"Number of cols: {df.shape[1]}")
    logging.info(f"Elapsed time: {timedelta(seconds=end_time - start_time)}")

    # Download dataframe as csv file
    df.to_csv(r'huggingface_models_dataset.csv', index=False)
    logging.info("File huggingface_models_dataset.csv has been downloaded in your current directory.")
    logging.info("The End.")
