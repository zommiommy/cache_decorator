
import pandas as pd

pandas_dict = {
    ".csv":{
        "load":pd.read_csv,
        "dump":lambda obj, path: obj.to_csv(path)
    },
    ".xlsx":{
        "load":pd.read_excel,
        "dump":lambda obj, path: obj.to_excel(path)
    },
}