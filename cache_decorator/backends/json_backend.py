import json
from typing import Dict, Any
from .backend_template import BackendTemplate

class JsonBackend(BackendTemplate):
    SUPPORTED_EXTENSIONS = [".json"]

    @staticmethod
    def can_serialize(obj_to_serialize: object, path:str) -> bool:
        """Returns if we can serialize the given type as the given extension"""
        return any(
            path.endswith(extension)
            for extension in JsonBackend.SUPPORTED_EXTENSIONS
        ) 

    @staticmethod
    def dump(obj_to_serialize: object, path:str) -> dict:
        """Serialize and save the object at the given path.
        If this backend needs extra informations to de-serialize data, it can 
        return them as a dictionary which will be serialized as a json."""   
        with open(path, "w") as f:  
            json.dump(obj_to_serialize, f)

    @staticmethod
    def can_deserialize(metadata: dict, path:str) -> bool:
        """Must return if the current backend can handle the type of data."""
        return any(
            path.endswith(extension)
            for extension in JsonBackend.SUPPORTED_EXTENSIONS
        ) 

    @staticmethod
    def load(metadata:dict, path:str) -> object:
        """Load the method at the given path. If the medod need extra
        informations it can read them form the metadata dictionary which is
        the return value of the dump method."""
        with open(path, "r") as f:  
            return json.load(f)