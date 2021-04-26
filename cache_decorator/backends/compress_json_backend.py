import compress_json
from .backend_template import BackendTemplate

class CompressJsonBackend(BackendTemplate):
    SUPPORTED_EXTENSIONS = [
        ".json",
        ".json.gz",
        ".json.bz",
        ".json.lzma",
    ]
    
    def __init__(self, load_kwargs, dump_kwargs):
        super(CompressJsonBackend, self).__init__(load_kwargs, dump_kwargs)

    @staticmethod
    def support_path(path:str) -> bool:
        return any(
            path.endswith(extension)
            for extension in CompressJsonBackend.SUPPORTED_EXTENSIONS
        ) 

    @staticmethod
    def can_deserialize(metadata: dict, path:str) -> bool:
        return CompressJsonBackend.support_path(path)

    @staticmethod
    def can_serialize(obj_to_serialize: object, path:str) -> bool:
        return CompressJsonBackend.can_deserialize({}, path)

    def dump(self, obj_to_serialize: object, path:str) -> dict:
        compress_json.dump(obj_to_serialize, path, **self._dump_kwargs)

    def load(self, metadata:dict, path:str) -> object:
        return compress_json.load(path, **self._load_kwargs)