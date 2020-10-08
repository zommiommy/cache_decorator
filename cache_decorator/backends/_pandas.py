try:
    import pandas as pd
except ModuleNotFoundError:
    pandas_dict = {}
    excel_dict = {}
else:
    pandas_dict = {
            ".csv"+compression:{
                    "load":pd.read_csv,
                    "dump":lambda obj, path: obj.to_csv(path)
                }
            for compression in ["", ".gz", ".bz2", ".zip", ".xz"]
        }

    try:
        import xlrd
    except ModuleNotFoundError:
        excel_dict = {}
    else:
        excel_dict = {
            ".xlsx":{
                    "load":pd.read_excel,
                    "dump":lambda obj, path: obj.to_excel(path)
                },
        }
    
pandas_dict = {**pandas_dict, **excel_dict}