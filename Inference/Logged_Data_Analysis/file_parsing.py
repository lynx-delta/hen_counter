 
import ast
import os

import pandas as pd


def flatten_dict(d, parent_key='', sep='_'):
    flattened = {}
    for k, v in d.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            flattened.update(flatten_dict(v, new_key, sep=sep))
        else:
            flattened[new_key] = v
    return flattened
    
def files_to_df(folder_path, ending='txt'):
    data_list = []
    for file in os.listdir(folder_path):
        if file.endswith(ending):
            filename, _ = os.path.splitext(file)
            file_with_path = os.path.join(folder_path, file)
            with open(file_with_path, 'r') as f:
                for line in f:
                    flattened = flatten_dict(ast.literal_eval(line))
                    flattened['filename'] = filename
                    data_list.append(flattened)
    
    df = pd.DataFrame(data_list)
    df['date'] = os.path.basename(folder_path)

    return df
                
    