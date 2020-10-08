try:
    from compress_pickle import dump, load
    extensions = [
        ".pkl",
        ".pkl.gz",
        ".pkl.bz",
        ".pkl.lzma",
        ".pkl.zip"
    ]
except ModuleNotFoundError:
    from pickle import dump, load
    extensions = [".pkl"]

pickle_dict = {
    extension : {
        "load":load,
        "dump":dump
    }
    for extension in extensions
}