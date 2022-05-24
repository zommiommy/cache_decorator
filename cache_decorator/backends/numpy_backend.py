
from this import d
from .backend_template import BackendTemplate
from .pandas_csv_backend import PandasCsvBackend
from typing import Dict, Any

try:
    import numpy as np

    class NumpyBackend(BackendTemplate):
        """Load and dump numpy types.

        .npy accpets a single np.array, np.ndarray, np.matrix.

        .npz accepths either a single array,
            a list of arrays
            or a dictionary of arrays
        """
        SUPPORTED_EXTENSIONS = [
            ".npy", ".npz"
        ] + ([] if PandasCsvBackend is None else list(PandasCsvBackend.SUPPORTED_EXTENSIONS.keys()))

        @staticmethod
        def support_path(path: str) -> bool:
            return any(
                path.endswith(extension)
                for extension in NumpyBackend.SUPPORTED_EXTENSIONS
            )

        @staticmethod
        def can_serialize(obj_to_serialize: object, path: str) -> bool:
            return NumpyBackend.support_path(path) and (
                isinstance(obj_to_serialize, np.ndarray)
                or isinstance(obj_to_serialize, dict) and all(
                    isinstance(e, np.ndarray)
                    for e in obj_to_serialize.values()
                )
                or isinstance(obj_to_serialize, (list, tuple)) and all(
                    isinstance(e, np.ndarray)
                    for e in obj_to_serialize
                )
            )

        @staticmethod
        def dump(obj_to_serialize: object, path: str) -> dict:
            if PandasCsvBackend is not None and PandasCsvBackend.support_path(path):
                import pandas as pd
                metadata = PandasCsvBackend().dump(
                    pd.DataFrame(obj_to_serialize),
                    path,
                )
                metadata["type"] = "numpy"
                return metadata
            if path.endswith(".npy"):
                with open(path, "wb") as f:
                    np.save(f, obj_to_serialize)
            elif isinstance(obj_to_serialize, dict):
                np.savez_compressed(path, **obj_to_serialize)
            elif isinstance(obj_to_serialize, (list, tuple, set)):
                np.savez_compressed(path, *obj_to_serialize)
            else:
                np.savez_compressed(path, obj_to_serialize)

            return {"type": str(type(obj_to_serialize))}

        @staticmethod
        def can_deserialize(metadata: dict, path: str) -> bool:
            pandas_test = PandasCsvBackend is not None and PandasCsvBackend.can_deserialize(
                metadata,
                path
            )
            return NumpyBackend.support_path(path) and not pandas_test or pandas_test and metadata["type"] == "numpy"

        @staticmethod
        def load(metadata: dict, path: str) -> object:
            if PandasCsvBackend is not None and PandasCsvBackend.support_path(path):
                return PandasCsvBackend.load(
                    metadata,
                    path,
                ).values
            if path.endswith(".npy"):
                with open(path, "rb") as f:
                    return np.load(f)

            # .npz
            objs = np.load(path)

            if metadata["type"] == str(dict):
                return dict(objs)
            elif metadata["type"] == str(list):
                return list([objs[x] for x in objs.files])
            elif metadata["type"] == str(tuple):
                return tuple([objs[x] for x in objs.files])
            else:
                # If it's just a value
                return objs[objs.files[0]]

except ModuleNotFoundError:
    NumpyBackend = None
