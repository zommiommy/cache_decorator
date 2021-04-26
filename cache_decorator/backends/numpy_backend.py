
from .backend_template import BackendTemplate

try:
    import numpy as np

    class NumpyBackend(BackendTemplate):
        """Load and dump numpy types.

        .npy accpets a single np.array, np.ndarray, np.matrix.

        .npz accepths either a single array,
            a list of arrays
            or a dictionary of arrays
        """
        SUPPORTED_EXTENSIONS = [".npy", ".npz"]

        def __init__(self, load_kwargs, dump_kwargs):
            # This is needed if we want to be able to save lists or dict of nparrays
            load_kwargs = load_kwargs.copy()
            load_kwargs.setdefault("allow_pickle", True)
            super(NumpyBackend, self).__init__(load_kwargs, dump_kwargs)

        @staticmethod
        def support_path(path:str) -> bool:
            return any(
                path.endswith(extension)
                for extension in NumpyBackend.SUPPORTED_EXTENSIONS
            ) 

        @staticmethod
        def can_serialize(obj_to_serialize: object, path:str) -> bool:
            return NumpyBackend.support_path(path)

        @staticmethod
        def can_deserialize(metadata: dict, path:str) -> bool:
            return NumpyBackend.support_path(path)

        def dump(self, obj_to_serialize: object, path:str) -> dict:
            if path.endswith(".npy"):
                with open(path, "wb") as f:
                    np.save(f, obj_to_serialize)

            if isinstance(obj_to_serialize, dict):
                np.savez_compressed(path, **obj_to_serialize)
            elif isinstance(obj_to_serialize, (list, tuple, set)):
                np.savez_compressed(path, *obj_to_serialize)
            else:
                np.savez_compressed(path, obj_to_serialize)
            
            return {"type":str(type(obj_to_serialize))}

        def load(self, metadata:dict, path:str) -> object:
            if path.endswith(".npy"):
                with open(path, "rb") as f:
                    return np.load(f)

            # .npz
            objs = np.load(path)
            
            if metadata["type"] == str(dict):
                return dict(objs)
            elif metadata["type"] == str(list):
                return list([objs[x] for x in objs.files])
            elif metadata["type"] == str(tuple):
                return tuple([objs[x] for x in objs.files])
            else:
                # If it's just a value
                return objs[objs.files[0]]

except ModuleNotFoundError:
    NumpyBackend = None

