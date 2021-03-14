
from .backend_template import BackendTemplate

try:
    import pandas as pd

    class PandasCsvBackend(BackendTemplate):

        def __init__(self, load_kwargs, dump_kwargs):
            load_kwargs = load_kwargs.copy()
            load_kwargs.setdefault("index_col", 0)
            super(PandasCsvBackend, self).__init__(load_kwargs, dump_kwargs)

        @staticmethod
        def does_the_extension_match(path: str) -> bool:
            return any(
                path.endswith(extension)
                for extension in [
                    ".csv",
                    ".csv.gz",
                    ".csv.bz2",
                    ".csv.xz",
                    ".csv.zip",
                ]
            ) 

        @staticmethod
        def can_deserialize(metadata: dict, path:str) -> bool:
            return PandasCsvBackend.does_the_extension_match(path) and metadata.get("type", None) == "pandas"

        @staticmethod
        def can_serialize(obj_to_serialize: object, path:str) -> bool:
            return PandasCsvBackend.does_the_extension_match(path) and isinstance(obj_to_serialize, pd.DataFrame)    

        def dump(self, obj_to_serialize: pd.DataFrame, path:str) -> dict: 
            obj_to_serialize.to_csv(path, **self._dump_kwargs)
            # Return the types of the columns to be saved as metadata
            return {
                "type":"pandas",
                "columns_types":{
                    column:str(type_val) 
                    for column, type_val in zip(
                        obj_to_serialize.columns, 
                        obj_to_serialize.dtypes
                    )
                }
            }

        def load(self, metadata:dict, path:str) -> object:
            df = pd.read_csv(path, **self._load_kwargs)
            # Convert back the types of the columns to the original ones
            df =  df.astype(metadata["columns_types"])
            return df

except ModuleNotFoundError:
    PandasCsvBackend = None