from ._json import json_dict
from ._numpy import numpy_dict
from ._pandas import pandas_dict
from ._pickle import pickle_dict

total_dict = {
    **json_dict,
    **pickle_dict,
    **numpy_dict,
    **pandas_dict,
}


def get_load_dump_from_path(path : str):
    for key, data in total_dict.items():
        if path.endswith(key):
            return data["load"], data["dump"]
    raise ValueError("The extension is not known. The available one are {}".format(
        list(total_dict.keys())))
