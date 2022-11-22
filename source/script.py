# Import libraries

import argparse
import logging
import pandas as pd
import time

from datetime import timedelta

from scraper import get_model_urls, get_model_attributes

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

    start_time = time.time()

    df = pd.DataFrame()
    for url in model_urls:
        model_attrs = get_model_attributes(url, custom_headers)
        if model_attrs:
            # Insert scrapped data as a new row in the dataframe
            df = pd.concat([df, pd.Series(model_attrs).to_frame().T])
        time.sleep(arguments.sleep)

    end_time = time.time()

    logging.info(f"Number of rows: {df.shape[0]}")
    logging.info(f"Number of cols: {df.shape[1]}")
    logging.info(f"Elapsed time: {timedelta(seconds=end_time - start_time)}")

    download_path = r'../dataset/'
    csv_name = r'huggingface_models_dataset.csv'
    # Download dataframe as csv file
    df.to_csv(download_path + csv_name, index=False)
    logging.info(f"File {csv_name} has been downloaded in {download_path}.")
    logging.info("The End.")
