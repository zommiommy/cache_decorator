
from .backend_template import BackendTemplate
import warnings

try:
    import pandas as pd

    # WHEN CHECKING FOR THE TYPE OF AN OBJECT IN A SERIES BEWARE THAT:
    #
    # series = pd.Series([1, 2, 3, 4])
    #
    # for s in series:
    #     print(str(type(s)))
    # outputs;
    #   `<class 'int'>
    #   `<class 'int'>
    #   `<class 'int'>
    #   `<class 'int'>
    #
    # str(type(series[2]))
    # outputs:
    #   "<class 'numpy.int64'>"

    def is_consistent(series: pd.Series) -> bool:
        """Check that all the values in the series are of the same type."""
        if series.dtype != "object":
            return True

        expected_type = str(type(series.values[0]))
        return all(
            expected_type == str(type(s))
            for s in series
        )

    def get_vector_dtype(series: pd.Series) -> str:
        """Get which type to use to serialize the type of the series"""
        t = str(series.dtype)
        if t == "object":
            return "str"
        return t

    common_message = (
        " contains values of multiple types therefore the data will be saved as required"
        " but we don't guarantee that"
        " they will be loaded as the same types as pandas does not support this.\n"
        "Consider using pickle (.pkl) or compress pickle (.pkl.gz, ...) to cache this complex type"
        " in a consistent manner."
    )

    class PandasCsvBackend(BackendTemplate):
        SUPPORTED_EXTENSIONS = {
            ".csv": ",",
            ".csv.gz": ",",
            ".csv.bz2": ",",
            ".csv.xz": ",",
            ".csv.zip": ",",
            ".tsv": "\t",
            ".tsv.gz": "\t",
            ".tsv.bz2": "\t",
            ".tsv.xz": "\t",
            ".tsv.zip": "\t",
            ".ssv": " ",
            ".ssv.gz": " ",
            ".ssv.bz2": " ",
            ".ssv.xz": " ",
            ".ssv.zip": " "
        }

        def __init__(self, load_kwargs, dump_kwargs):
            load_kwargs = load_kwargs.copy()
            load_kwargs.setdefault("index_col", 0)
            super(PandasCsvBackend, self).__init__(load_kwargs, dump_kwargs)

        @staticmethod
        def support_path(path: str) -> bool:
            return any(
                path.endswith(extension)
                for extension in PandasCsvBackend.SUPPORTED_EXTENSIONS
            )

        @staticmethod
        def can_deserialize(metadata: dict, path: str) -> bool:
            return PandasCsvBackend.support_path(path) and metadata.get("type", None) == "pandas"

        @staticmethod
        def can_serialize(obj_to_serialize: object, path: str) -> bool:
            return PandasCsvBackend.support_path(path) and isinstance(obj_to_serialize, pd.DataFrame)

        def dump(self, obj_to_serialize: pd.DataFrame, path: str) -> dict:

            for column in obj_to_serialize.columns:
                if not is_consistent(obj_to_serialize[column]):
                    warnings.warn("The column '{}'".format(
                        column) + common_message)

            if not is_consistent(obj_to_serialize.index):
                warnings.warn("The index" + common_message)

            if not is_consistent(obj_to_serialize.columns):
                warnings.warn("The column names" + common_message)

            obj_to_serialize.to_csv(
                path,
                sep=self.SUPPORTED_EXTENSIONS[
                    next(
                        x
                        for x in self.SUPPORTED_EXTENSIONS
                        if path.endswith(x)
                    )
                ],
                **self._dump_kwargs
            )

            # Return the types of the columns to be saved as metadata
            return {
                "type": "pandas",
                "columns_types": {
                    column: get_vector_dtype(obj_to_serialize[column])
                    for column in obj_to_serialize.columns
                },
                "index_type": get_vector_dtype(obj_to_serialize.index),
                "columns_names_type": get_vector_dtype(obj_to_serialize.columns),
            }

        def load(self, metadata: dict, path: str) -> object:
            df = pd.read_csv(
                path,
                sep=self.SUPPORTED_EXTENSIONS[
                    next(
                        x
                        for x in self.SUPPORTED_EXTENSIONS
                        if path.endswith(x)
                    )
                ],
                **self._load_kwargs
            )
            # Convert back the types of the columns to the original ones
            df = df.astype(metadata["columns_types"])
            df.index = df.index.astype(metadata["index_type"])
            df.columns = df.columns.astype(metadata["columns_names_type"])
            return df

except ModuleNotFoundError:
    PandasCsvBackend = None
