from typing import Dict, Any
import compress_json
from .backend_template import BackendTemplate

class CompressJsonBackend(BackendTemplate):
    SUPPORTED_EXTENSIONS = [
        ".json",
        ".json.gz",
        ".json.bz",
        ".json.lzma",
    ]

    @staticmethod
    def can_serialize(obj_to_serialize: object, path:str) -> bool:
        return any(
            path.endswith(extension)
            for extension in CompressJsonBackend.SUPPORTED_EXTENSIONS
        ) 

    @staticmethod
    def dump(obj_to_serialize: object, path:str) -> dict:
        compress_json.dump(obj_to_serialize, path)

    @staticmethod
    def can_deserialize(metadata: dict, path:str) -> bool:
        return any(
            path.endswith(extension)
            for extension in CompressJsonBackend.SUPPORTED_EXTENSIONS
        ) 

    @staticmethod
    def load(metadata:dict, path:str) -> object:
        return compress_json.load(path)

