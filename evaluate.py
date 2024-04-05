from sklearn.metrics import r2_score
import json
import yaml
import os
import pandas as pd
import numpy as np

with open('params.yaml') as f:
    params = yaml.safe_load(f)

daily_fields = params['prepare']['daily_fields']
monthly_fields = params['prepare']['monthly_fields']

def get_files():
    folders = os.listdir('data')
    files = []
    for folder in folders:
        base = 'data/'+folder + '/'
        files.extend([base + file  for file in os.listdir(base)])
    return files

def evaluate_file(file):
    gt_base = 'outputs/prepare/'
    computed_base = 'outputs/process/'
    gt = pd.read_csv(f'{gt_base}{file}')
    computed = pd.read_csv(f'{computed_base}{file}')
    df = pd.merge(gt,computed,on='MONTH')
    scores = {}
    for d,m in zip(daily_fields,monthly_fields):
        c = d.replace('Daily','MonthlyGT')
        g = m
        score = r2_score(df[g],df[c])
        scores[d] = score
    return scores


if __name__ == '__main__':
    files = get_files()
    all_scores = {}
    for file in files:
        scores = evaluate_file(file)
        all_scores[file.strip('.csv')] = scores

    with open('outputs/scores.json','w') as f:
        json.dump(all_scores,f,indent=4)