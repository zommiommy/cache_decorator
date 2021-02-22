from ..exception import SerializationException

try:
    from compress_json import load, dump
    extensions = ["", ".gz", ".bz", ".lzma"]
except ModuleNotFoundError:
    from json import dump, load
    extensions = [""]

def decorated_dump(obj, path):
    # This checks only the first layer,
    # {"a": np.array([1, 2, 3])} would break the check
    # also json MUST have the keys as strings,
    # thus {1:1} would also pass the check but break the serializtion
    if type(obj) not in [
            str,
            dict,
            list,
            int,
            float,
        ]:
        raise SerializationException(
            "Cannot serialize as json an object of type %s"%type(obj),
            path, obj
        )
    dump(obj, path)

json_dict = {
    ".json" + extension:{
        "load":load,
        "dump":decorated_dump,
    }
    for extension in extensions
}