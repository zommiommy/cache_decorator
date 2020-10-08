try:
    from compress_json import load, dump
    extensions = ["", ".gz", ".bz", ".lzma"]
except ModuleNotFoundError:
    from json import dump, load
    extensions = [""]

json_dict = {
    ".json" + extension:{
        "load":load,
        "dump":dump,
    }
    for extension in extensions
}