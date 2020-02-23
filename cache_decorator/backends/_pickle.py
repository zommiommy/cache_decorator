
from compress_pickle import dump, load

pickle_dict = {
    extension : {
        "load":load,
        "dump":dump
    }
    for extension in [
        ".pkl",
        ".pkl.gz",
        ".pkl.bz",
        ".pkl.lzma",
        ".pkl.zip"
    ]
}