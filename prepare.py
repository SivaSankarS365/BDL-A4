import os
import pandas as pd
import numpy as np
import yaml

with open('params.yaml') as f:
    params = yaml.safe_load(f)

monthly_fields = params['prepare']['monthly_fields']


def get_files():
    folders = os.listdir('data')
    files = []
    for folder in folders:
        base = 'data/'+folder + '/'
        files.extend([base + file  for file in os.listdir(base)])
    return files

def strip_strings_and_convert_to_float(df,cols):
    for col in cols:
        df[col] = df[col].str.replace('[a-zA-Z]','',regex=True)
    df.replace({'':np.nan},inplace=True)
    df.dropna(inplace=True)
    for col in cols:
        df[col] = df[col].astype(float)
    return df

def prepare_gt(file):
    df = pd.read_csv(file,low_memory=False)
    monthly = df.loc[df[monthly_fields].drop_duplicates().index, ['DATE'] + monthly_fields].dropna()
    monthly = strip_strings_and_convert_to_float(monthly,monthly_fields)
    monthly['MONTH'] = monthly.DATE.apply(lambda x: pd.to_datetime(x).month)
    df = monthly[['MONTH'] + monthly_fields]
    os.makedirs('outputs/prepare/',exist_ok=True)
    df.to_csv(f'outputs/prepare/{file.split("/")[-1]}',index=False)

files = get_files()
for file in files:
    prepare_gt(file)