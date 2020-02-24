
import pandas as pd

pandas_dict = {
    **{
        ".csv"+compression:{
                "load":pd.read_csv,
                "dump":lambda obj, path: obj.to_csv(path)
            }
        for compression in ["", ".gz", ".bz2", ".zip", ".xz"]
    },
    ".xlsx":{
        "load":pd.read_excel,
        "dump":lambda obj, path: obj.to_excel(path)
    },
}