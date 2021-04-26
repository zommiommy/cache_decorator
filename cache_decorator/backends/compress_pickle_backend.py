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

    def __init__(self, load_kwargs, dump_kwargs):
        super(CompressPickleBackend, self).__init__(load_kwargs, dump_kwargs)

    @staticmethod
    def support_path(path:str) -> bool:
        return any(
            path.endswith(extension)
            for extension in CompressPickleBackend.SUPPORTED_EXTENSIONS
        ) 

    @staticmethod
    def can_serialize(obj_to_serialize: object, path:str) -> bool:
        return CompressPickleBackend.support_path(path)

    @staticmethod
    def can_deserialize(metadata: dict, path:str) -> bool:
        return CompressPickleBackend.support_path(path)

    def dump(self, obj_to_serialize: object, path:str) -> dict:
        pickle_dump(obj_to_serialize, path, **self._dump_kwargs)

    def load(self, metadata:dict, path:str) -> object:
        return pickle_load(path, **self._load_kwargs)