from typing import Dict, Any
from compress_pickle import dump as pickle_dump, load as pickle_load
from .backend_template import BackendTemplate

class CompressPickleBackend(BackendTemplate):
    SUPPORTED_EXTENSIONS = [
        ".pkl",
        ".pkl.gz",
        ".pkl.bz",
        ".pkl.lzma",
        ".pkl.zip",
    ]

    @staticmethod
    def can_serialize(obj_to_serialize: object, path:str) -> bool:
        return any(
            path.endswith(extension)
            for extension in CompressPickleBackend.SUPPORTED_EXTENSIONS
        ) 

    @staticmethod
    def dump(obj_to_serialize: object, path:str) -> dict:
        pickle_dump(obj_to_serialize, path)

    @staticmethod
    def can_deserialize(metadata: dict, path:str) -> bool:
        return any(
            path.endswith(extension)
            for extension in CompressPickleBackend.SUPPORTED_EXTENSIONS
        ) 

    @staticmethod
    def load(metadata:dict, path:str) -> object:
        return pickle_load(path)