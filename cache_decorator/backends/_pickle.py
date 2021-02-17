# Notes:
# Compress pickle do accept paths as file arguments
# BUT STANDARD PICKLE DOES NOT.

try:
    from compress_pickle import dump, load

    pickle_dict = {
        extension : {
            "load":load,
            "dump":dump
        }
        for extension in [
            ".pkl.gz",
            ".pkl.bz",
            ".pkl.lzma",
            ".pkl.zip"
        ]
    }
except ModuleNotFoundError:
    pickle_dict = {}

from pickle import dump as pickle_dump, load as pickle_load
extensions = [".pkl"]

def default_dump(value, path):
    with open(path, "wb") as f:
        pickle_dump(value, f)

def default_load(path):
    with open(path, "rb") as f:
        return pickle_load(f)

pickle_dict[".pkl"] = {
    "load":default_load,
    "dump":default_dump
}