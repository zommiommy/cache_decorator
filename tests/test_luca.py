import os
import numpy as np
import pandas as pd
from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test

@Cache(cache_path="test_cache/{x}/mister_fisco.csv")
def luca_func(x):
    url = "https://www.misterfisco.it/i-codici-catastali-dei-comuni-in-ordine-alfabetico-per-comune/"
    table = pd.read_html(url)[0]
    table.columns = table.iloc[0]
    table.drop(index=0, inplace=True)
    table.rename(columns={
        "Comune": "municipality",
        "Provincia": "province",
        "Codice": "code"
    }, inplace=True)
    sleep(1)
    return table

def test_luca():
    # Here we cannot use standard_test_dataframes
    # Because it contains NaNs OF COURSE
    standard_test(luca_func)
