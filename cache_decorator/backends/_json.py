try:
    from compress_json import load, dump

    json_dict = {
        ".json" + extension:{
            "load":load,
            "dump":dump,
        }
        for extension in ["", ".gz", ".bz", ".lzma"]
        
    }
except ModuleNotFoundError:
    from json import dump, load
    json_dict = {
        ".json":{
            "load":load,
            "dump":dump
        }
    }