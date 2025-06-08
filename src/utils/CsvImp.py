import sys
from datetime import date

import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))


def CsvWriter(file: str, dict_list: list[dict[str, str]]):
    file = f'{project_root}/CsvFiles/{file}.csv'
    FileExists(file)
    df = pd.DataFrame(dict_list)
    df["Date"] = date.today()
    df.to_csv(file, header=True, index=False)
    print(f'file location :{file}')
    return


def FileExists(file):
    if os.path.exists(file) and os.path.isfile(file):
        os.remove(file)
        print("file overwritten")


def get_page_range():
    """
    Determines FIRST_PAGE and LAST_PAGE from command-line arguments.
    - No args: returns (1, 10)
    - One arg: returns (1, int(arg1))
    - Two args: returns (int(arg1), int(arg2))
    """
    if len(sys.argv) == 1:
        return 1, 10
    elif len(sys.argv) == 2:
        return 1, int(sys.argv[1])
    else:
        return int(sys.argv[1]), int(sys.argv[2])


def merge_multiple_csv(files, output_file):
    """
    Merges multiple CSV files with the same columns into a single output file.

    Args:
        files (list of str): List of file paths to CSVs.
        output_file (str): Path for the merged CSV output.
    """
    try:
        dataframes = [pd.read_csv(f) for f in files]

        merged_df = pd.concat(dataframes, ignore_index=True)
        duplicates = merged_df["Name"].value_counts()
        duplicates = duplicates[duplicates > 1]
        print(duplicates)

        merged_df.to_csv(f'original_scrapped_{output_file}', index=False)

        column_name = "MarketCap($)"
        merged_df[column_name] = merged_df[column_name].astype(str).apply(convert)
        merged_df = merged_df.sort_values(by=column_name, ascending=False)
        merged_df.to_csv(f'modified_{output_file}', index=False)


    except Exception as e:
        print(f"Error merging CSV files: {e}")


def convert(value):
    try:
        if value == 'na':
            return 0
        value = value.replace('$', '').replace(',', '').strip().upper()

        if value.endswith('B'):
            return float(value[:-1]) * 1_000_000_000
        elif value.endswith('M'):
            return float(value[:-1]) * 1_000_000
        elif value.endswith('K'):
            return float(value[:-1]) * 1_000
        else:
            return float(value)  # if it's already a plain number
    except Exception:
        return -1  # or `float('nan')`


if __name__ == '__main__':
    files = ["parallel_250608-182255_1-50.csv", "parallel_250608-184150_51-98.csv"]

    files = [f'{project_root}/CsvFiles/{file}' for file in files]
    merge_multiple_csv(files, "98_pages_coins.csv")
