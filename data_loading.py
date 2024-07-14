import os
import pandas as pd

def load_data(file_path):
    path = os.getcwd()
    file_map = {
        '1': 'data/Germany_MA.xlsx',
        '2': 'data/Germany_Reimbursement.xlsx',
        '3': 'data/Europe_MA.xlsx',
        '4': 'data/USA_MA.xlsx',
        '5': 'data/Scotland_MA.xlsx',
        '6': 'data/Scotland_Reimbursement.xlsx',
        '7': 'data/Australia_MA.xlsx',
        '8': 'data/Australia_Reimbursement.xlsx',
        '9': 'data/UK_Reimbursement.xlsx'
    }
    file_path = file_map.get(file_path, 'data/UK_MA.xlsx')
    file_path = os.path.join(path, file_path)
    df = pd.read_excel(file_path)
    df['Date of decision'] = pd.to_datetime(df['Date of decision'], dayfirst=True, errors='coerce')
    return df

def load_clinical_trials_data():
    path = os.getcwd()
    file_path = 'data/Clinical_Trials.xlsx'
    file_path = os.path.join(path, file_path)
    df = pd.read_excel(file_path)
    return df
