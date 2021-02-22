from ..exception import SerializationException

try:
    import pandas as pd
except ModuleNotFoundError:
    pandas_dict = {}
    excel_dict = {}
else:
    def to_csv(obj, path):
        if type(obj) is not pd.DataFrame:
            raise SerializationException(
                "Cannot serialize as csv anything that's not a pandas Dataframe.",
                path, obj
            )

        obj.to_csv(path)

    pandas_dict = {
            ".csv"+compression:{
                    "load":lambda path: pd.read_csv(path, index_col=0),
                    "dump":to_csv
                }
            for compression in ["", ".gz", ".bz2", ".zip", ".xz"]
        }

    try:
        import xlrd
    except ModuleNotFoundError:
        excel_dict = {}
    else:

        def to_xlsx(obj, path):
            if type(obj) is not pd.DataFrame:
                raise SerializationException(
                    "Cannot serialize as csv anything that's not a pandas Dataframe.",
                    path, obj
                )
                
            obj.to_excel(path)

        excel_dict = {
            ".xlsx":{
                    "load":pd.read_excel,
                    "dump":to_xlsx
                },
        }
    
pandas_dict = {**pandas_dict, **excel_dict}