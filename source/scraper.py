# Import libraries

import logging
import json
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
    modelHeaderActions = model_soup.find('div', attrs={'data-target': 'ModelHeaderActions'})
    if modelHeaderActions is None:
        print(f'Error in ModelHeaderActions: {url}')
    else:
        data_props = json.loads(modelHeaderActions.attrs['data-props'].replace(r'\\"', r'\"'))
        target_fields = ['author', 'id', 'cardExists', 'lastModified', 'likes']
        for field in target_fields:
            if field in data_props['model']:
                fields[field] = data_props['model'][field]

        tag_objs = data_props['model']['tag_objs']
        for tag_obj in tag_objs:
            # print(tag_obj) # uncomment this for better understanding of what is going on
            if not tag_obj['type'] in fields:
                fields[tag_obj['type']] = []
            fields[tag_obj['type']].append(tag_obj['id'])
            if tag_obj['type'] == 'pipeline_tag':
                fields['subType'] = tag_obj['subType']

    return fields
