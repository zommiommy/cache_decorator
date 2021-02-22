from ..exception import SerializationException

try:
    import numpy as np
except ModuleNotFoundError:
    numpy_dict = {}
else:
    def load_npz(path):
        with open(path, "rb") as f:
            objs = np.load(f)
            return [objs[k] for k in objs.files]

    def save_npz(objs, path):
        with open(path, "wb") as f:
            np.savez(f, *objs)

    def save_compressed_npz(objs, path):
        with open(path, "wb") as f:
            np.savez_compressed(f, *objs)

    def load_npy(path):
        with open(path, "rb") as f:
            return np.load(f)

    def dump_npy(obj, path):
        if type(obj) == list:
            raise SerializationException(
                    "Cannot save a list as .npy, maybe you meant .npz to save a list of numpy arrays?\n"
                    "Otherwise we cannot save a list as a numpy array but you must manually cast it in the function"
                    " because otherwise the function would return different types depending on wheater the value is "
                    "computed or loaded from cache.", 
                    path, obj
                )

        if type(obj) not in [
                np.array,
                np.ndarray,
                np.matrix,
            ]:
            raise SerializationException("The given object of type %s is not compatible with the extension .npy."%type(obj), path, obj)

        with open(path, "wb") as f:
            np.save(f, obj)

    numpy_dict = {
        "npy":{
            "load":load_npy,
            "dump":dump_npy
        },
        "npz":{
            "load":load_npz,
            "dump":save_compressed_npz
        }
    }