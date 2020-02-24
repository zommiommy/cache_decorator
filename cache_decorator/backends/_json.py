
from json import dump, load

def json_dump(obj, path):
    with open(path, "w") as f:
        dump(obj, f)

def json_load (path):
    with open(path, "r") as f:
        return load(f)

json_dict = {
    ".json":{
        "load":json_load,
        "dump":json_dump,
    },
}