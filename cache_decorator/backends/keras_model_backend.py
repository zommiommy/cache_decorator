"""Backend for Keras models."""
import os
import tarfile
import tempfile
from .backend_template import BackendTemplate


try:

    def create_tar(src_dir, tar_file, extension):
        with tarfile.open(tar_file, "w:%s" % extension) as tar_handle:
            for root, dirs, files in os.walk(src_dir):
                for file in files:
                    p = os.path.join(root, file)
                    tar_handle.add(p, arcname=p[len(src_dir) :])

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
        """Backend for Keras models."""

        SUPPORTED_EXTENSIONS = [
            ".keras.tar",
            ".keras.tar.gz",
            ".keras.tar.bz2",
            ".keras.tar.xz",
        ]

        @staticmethod
        def support_path(path: str) -> bool:
            return any(
                path.endswith(extension)
                for extension in KerasModelBackend.SUPPORTED_EXTENSIONS
            )

        @staticmethod
        def can_deserialize(metadata: dict, path: str) -> bool:
            return KerasModelBackend.support_path(path)

        @staticmethod
        def can_serialize(obj_to_serialize: object, path: str) -> bool:
            return KerasModelBackend.support_path(path)

        def dump(self, obj_to_serialize: "Model", path: str) -> dict:
            from tensorflow.keras.models import (
                save_model,
            )  # pylint: disable=import-outside-toplevel

            with tempfile.TemporaryDirectory() as tmpdirname:
                save_model(obj_to_serialize, tmpdirname, **self._dump_kwargs)
                create_tar(tmpdirname, path, get_extension(path))

        def load(self, metadata: dict, path: str) -> object:
            from tensorflow.keras.models import (
                load_model,
            )  # pylint: disable=import-outside-toplevel

            with tempfile.TemporaryDirectory() as tmpdirname:
                with tarfile.open(path, "r:*") as tar_handle:
                    tar_handle.extractall(tmpdirname)
                return load_model(tmpdirname, **self._load_kwargs)


# We need to check both for `ModuleNotFoundError`, where
# simply the TensorFlow package is not installed, and
# a more obscure `TypeError` caused by occasional internal
# errors of TensorFlow when it is not properly installed.
except (ModuleNotFoundError, TypeError):
    KerasModelBackend = None
