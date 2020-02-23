
import os

def cache_logic(path, func, args, kwargs, load, dump):
    # ensure that the cache folder exist
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # If the file exist, load it
    if os.path.exists(path):
        print("Loading cache at {}".format(path))
        return load(path)
    # else call the function
    result = func(*args, **kwargs)
    # and save the result
    dump(result, path)
    return result


