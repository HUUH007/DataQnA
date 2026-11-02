import pandas as pd
from pathlib import Path


def schema_extract(
        file: Path,
) -> str:

    def get_csv_header_dtypes(
        df: pd.DataFrame            
    ) -> dict:
        dtype_series = df.dtypes
        dtype_dict = dtype_series.to_dict()
        return dtype_dict

    df = pd.read_csv(file, nrows=1000, encoding="utf-8-sig")
    header = get_csv_header_dtypes(df)
    header_str = f"Table name: {file.stem} \n"
    for col, dtype in header.items():
        header_str += f"{col} ({dtype}) \n"
    return header_str

