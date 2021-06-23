import os
import numpy as np
import pandas as pd
from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_dataframes

@Cache(cache_path="test_cache/mister_fisco.csv")
def luca_func():
    url = "https://www.misterfisco.it/i-codici-catastali-dei-comuni-in-ordine-alfabetico-per-comune/"
    table = pd.read_html(url)[0]
    table.columns = table.iloc[0]
    table.drop(index=0, inplace=True)
    table.rename(columns={
        "Comune": "municipality",
        "Provincia": "province",
        "Codice": "code"
    }, inplace=True)
    return table

def test_luca():
    get_mister_fisco_codes()
    os.remove("test_cache/mister_fisco.csv")
    os.remove("test_cache/mister_fisco.csv.metadata")
