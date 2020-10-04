# by Richi Rod AKA @richionline / falken20

import base64
import json
import pandas as pd
import logging
import os
import sys


class B64Utils:
    @staticmethod
    def file_from_base64(data, file_name):
        """
        Decodes base64 string from `data` and save it as binary file in `file_name`.
        """
        with open(file_name, "wb") as fh:
            fh.write(base64.b64decode(data))
        print("Saved to '{}'".format(file_name))


class JSONUtils:
    @staticmethod
    def pprint(origin_json):
        """
        It pretty prints the `origin_json` to show on the screen.
        """
        print(json.dumps(origin_json, indent=4, sort_keys=True))


def get_float(chain_literal):
    """ From a chain get the float in the first position of split(), in other case return 0.0 """
    try:
        num_float = float(chain_literal.split()[0])
    except ValueError:
        num_float = float(0)
    finally:
        return num_float


def scrap_web(url):
    """
    For getting data weather of a specific url
    :param url: The url of a specific web
    """
    try:
        data = pd.read_html(url)
        df = data[0]

        logging.info(f'{os.getenv("ID_LOG", "")} url scrapping: {url}')
        logging.debug(f'{os.getenv("ID_LOG", "")} Data to scrap:\n {data[0]}')

        # Cleaning the info it doesn't neccesary
        df = df.drop([4], axis=1)  # axis is the column name
        df = df.drop([0, 1, 2, 3, 4, 5])

        # Get seveal rows and cols
        df = df.iloc[0:6, [0, 1]]

        # We can change the name of the columns
        df.columns = ('Parameter', 'Value')

        # Clean and restore the index number because it is kind of
        # annoying but it is not necessary
        df = df.reset_index(drop=True)

        logging.info(f'{os.getenv("ID_LOG", "")} Data scrapped:\n {df}')

        return df

    except Exception as err:
        logging.error(f'{os.getenv("ID_LOG", "")} ERROR scrapping web at line {sys.exc_info()[2].tb_lineno}: {err}')
        return None        