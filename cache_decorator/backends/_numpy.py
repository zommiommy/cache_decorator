import numpy as np


def load_npz(path):
    obj = np.load(path)
    keys = list(obj.keys())
    keys.sort()
    return tuple(
        obj[key]
        for key in keys
    )

def save_npz(list_of_arrays, path):
    np.savez(path, **dict(enumerate(list_of_arrays)))



numpy_dict = {
    "npy":{
        "load":np.load,
        "dump":np.save
    },
    "npz":{
        "load":load_npz,
        "dump":save_npz
    }
}