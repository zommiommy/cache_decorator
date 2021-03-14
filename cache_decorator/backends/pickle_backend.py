import pickle
from pickle import dump as pickle_dump, load as pickle_load
from .backend_template import BackendTemplate

class PickleBackend(BackendTemplate):

    def __init__(self, load_kwargs, dump_kwargs):
        super(PickleBackend, self).__init__(load_kwargs, dump_kwargs)

    @staticmethod
    def can_serialize(obj_to_serialize: object, path:str) -> bool:
        return path.endswith(".pkl")

    @staticmethod
    def can_deserialize(metadata: dict, path:str) -> bool:
        return path.endswith(".pkl")

    def dump(self, obj_to_serialize: object, path:str) -> dict:
        with open(path, "wb") as f:
            pickle_dump(obj_to_serialize, f, **self._dump_kwargs)

    def load(self, metadata:dict, path:str) -> object:
        with open(path, "rb") as f:
            return pickle_load(f, **self._load_kwargs)