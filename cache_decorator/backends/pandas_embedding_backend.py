
from .backend_template import BackendTemplate
from typing import Dict, Any

try:
    import pickle
    import tarfile
    import numpy as np
    import pandas as pd
    from io import BytesIO

    def is_numeric_dataframe(df: pd.DataFrame) -> bool:
        """Check if all the columns have numerical data types."""
        return all(
            str(dtype).startswith(("int", "float"))
            for dtype in df.dtypes
        )

    class PandasEmbeddingBackend(BackendTemplate):
        """This format is optimzied to compress datafarmes that contains ONLY numerical values.
        For .gz and .bz2 you can use the load_kwarg `compresslevel` to set the 
        compression level (default 9). For .xz you can use the load_kwarg preset
        to set the compression level."""

        SUPPORTED_EXTENSIONS = {
            ".embedding":":",
            ".embedding.gz":":gz",
            ".embedding.bz2":":bz2",
            ".embedding.xz":":xz",
        }
        
        @staticmethod
        def support_path(path: str) -> bool:
            return any(
                path.endswith(extension)
                for extension in PandasEmbeddingBackend.SUPPORTED_EXTENSIONS
            )

        @staticmethod
        def can_deserialize(metadata: dict, path: str) -> bool:
            return PandasEmbeddingBackend.support_path(path)

        @staticmethod
        def can_serialize(obj_to_serialize: object, path: str) -> bool:
            return PandasEmbeddingBackend.support_path(path) and \
                    isinstance(obj_to_serialize, pd.DataFrame) and \
                    is_numeric_dataframe(obj_to_serialize)

        @staticmethod
        def dump(obj_to_serialize: pd.DataFrame, path: str) -> dict:

            open_prefix = next(
                v
                for k, v in PandasEmbeddingBackend.SUPPORTED_EXTENSIONS.items()
                if path.endswith(k)
            )

            with tarfile.open(path, mode="w" + open_prefix) as tar:
                data = pickle.dumps(obj_to_serialize.columns)
                infos = tarfile.TarInfo("columns.pkl")
                infos.size = len(data)
                tar.addfile(infos, fileobj=BytesIO(data))
                
                data = pickle.dumps(obj_to_serialize.index)
                infos = tarfile.TarInfo("index.pkl")
                infos.size = len(data)
                tar.addfile(infos, fileobj=BytesIO(data))
                
                f = BytesIO()
                np.save(f, obj_to_serialize.values)
                infos = tarfile.TarInfo("values.npy")
                infos.size = f.tell()
                f.seek(0)
                tar.addfile(infos, fileobj=f)


            # Return the types of the columns to be saved as metadata
            return {
                "type": "pandas_embedding",
            }

        @staticmethod
        def load(metadata: dict, path: str) -> object:
            with tarfile.open(path, mode="r") as tar:
                columns = pickle.load(tar.extractfile("columns.pkl"))
                index = pickle.load(tar.extractfile("index.pkl"))
                
                array_file = BytesIO()
                array_file.write(tar.extractfile("values.npy").read())
                array_file.seek(0)
                values = np.load(array_file)
                
                return pd.DataFrame(values, columns=columns, index=index)

except ModuleNotFoundError:
    PandasEmbeddingBackend = None
