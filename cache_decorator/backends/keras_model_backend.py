import os
import tarfile
import tempfile
from typing import Dict, Any
from .backend_template import BackendTemplate

try:
    from tensorflow.keras.models import Model, save_model, load_model

    def create_tar(src_dir, tar_file, extension):
        with tarfile.open(tar_file, "w:%s"%extension) as tar_handle:
            for root, _dirs, files in os.walk(src_dir):
                for file in files:
                    p = os.path.join(root, file)
                    tar_handle.add(p, arcname=p[len(src_dir):])

    def get_extension(path):
        if path.endswith(".tar"):
            return ""
        elif path.endswith(".tar.gz"):
            return "gz"
        elif path.endswith(".tar.bz2"):
            return "bz2"
        elif path.endswith(".tar.xz"):
            return "xz"
        raise ValueError("Cannot find the right extension")

    class KerasModelBackend(BackendTemplate):
        SUPPORTED_EXTENSIONS = [
            ".keras.tar",
            ".keras.tar.gz",
            ".keras.tar.bz2",
            ".keras.tar.xz",
        ]
            
        @staticmethod
        def can_deserialize(metadata: dict, path:str) -> bool:
            return any(
                path.endswith(extension)
                for extension in KerasModelBackend.SUPPORTED_EXTENSIONS
            ) 

        @staticmethod
        def can_serialize(obj_to_serialize: object, path:str) -> bool:
            return any(
                path.endswith(extension)
                for extension in KerasModelBackend.SUPPORTED_EXTENSIONS
            ) 

        @staticmethod
        def dump(obj_to_serialize: Model, path:str) -> dict: 
            with tempfile.TemporaryDirectory() as tmpdirname:
                save_model(obj_to_serialize, tmpdirname)
                create_tar(tmpdirname, path, get_extension(path))

        @staticmethod
        def load(metadata:dict, path:str) -> object:
            with tempfile.TemporaryDirectory() as tmpdirname:
                with tarfile.open(path, "r:*") as tar_handle:
                    tar_handle.extractall(tmpdirname)
                return load_model(tmpdirname)

except ModuleNotFoundError:
    KerasModelBackend = None