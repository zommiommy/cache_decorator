import json
from .backend_template import BackendTemplate

class JsonBackend(BackendTemplate):
    SUPPORTED_EXTENSIONS = [".json"]

    def __init__(self, load_kwargs, dump_kwargs):
        super(JsonBackend, self).__init__(load_kwargs, dump_kwargs)
        
    @staticmethod
    def support_path(path:str) -> bool:
        return any(
            path.endswith(extension)
            for extension in JsonBackend.SUPPORTED_EXTENSIONS
        ) 

    @staticmethod
    def can_deserialize(metadata: dict, path:str) -> bool:
        """Must return if the current backend can handle the type of data."""
        return JsonBackend.support_path(path)

    @staticmethod
    def can_serialize(obj_to_serialize: object, path:str) -> bool:
        """Returns if we can serialize the given type as the given extension"""
        return JsonBackend.support_path(path)

    def dump(self, obj_to_serialize: object, path:str) -> dict:
        """Serialize and save the object at the given path.
        If this backend needs extra informations to de-serialize data, it can 
        return them as a dictionary which will be serialized as a json."""   
        with open(path, "w") as f:  
            json.dump(obj_to_serialize, f, **self._dump_kwargs)

    def load(self, metadata:dict, path:str) -> object:
        """Load the method at the given path. If the medod need extra
        informations it can read them form the metadata dictionary which is
        the return value of the dump method."""
        with open(path, "r") as f:  
            return json.load(f, **self._load_kwargs)