import pandas as pd
import os


def CsvWriter(file:str, diction):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

    file = f'{project_root}/CsvFiles/{file}.csv'
    FileExists(file)
    df = pd.DataFrame(diction)
    df.to_csv(file, header=True, index=False)
    print(f'file location :{file}')
    return


def FileExists(file):
    if os.path.exists(file) and os.path.isfile(file):
        os.remove(file)
        print("file overwritten")
