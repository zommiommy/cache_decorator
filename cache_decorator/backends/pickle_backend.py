from typing import Dict, Any
from pickle import dump as pickle_dump, load as pickle_load
from .backend_template import BackendTemplate

class PickleBackend(BackendTemplate):
    SUPPORTED_EXTENSIONS = [".pkl"]

    @staticmethod
    def support_path(path:str) -> bool:
        return any(
            path.endswith(extension)
            for extension in PickleBackend.SUPPORTED_EXTENSIONS
        ) 

    @staticmethod
    def can_serialize(obj_to_serialize: object, path:str) -> bool:
        return PickleBackend.support_path(path)

    @staticmethod
    def can_deserialize(metadata: dict, path:str) -> bool:
        return PickleBackend.support_path(path)

    @staticmethod
    def dump(obj_to_serialize: object, path:str) -> dict:
        with open(path, "wb") as f:
            pickle_dump(obj_to_serialize, f)

    @staticmethod
    def load(metadata:dict, path:str) -> object:
        with open(path, "rb") as f:
            return pickle_load(f)