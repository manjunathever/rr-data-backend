import pandas as pd
from collections import OrderedDict

def filter_data(df, column_name, search_term, start_date, end_date):
    if start_date and end_date:
        start_date = pd.to_datetime(start_date, errors='coerce')
        end_date = pd.to_datetime(end_date, errors='coerce')
        df = df[(df['Date of decision'] >= start_date) & (df['Date of decision'] <= end_date)]
    elif start_date:
        start_date = pd.to_datetime(start_date, errors='coerce')
        df = df[df['Date of decision'] >= start_date]
    elif end_date:
        end_date = pd.to_datetime(end_date, errors='coerce')
        df = df[df['Date of decision'] <= end_date]

    if column_name and search_term:
        df = df[df[column_name].astype(str).str.contains(search_term, case=False, na=False)]

    df = df.dropna(axis=1, how='all')
    df = df.where(pd.notnull(df), None)
    result = [OrderedDict(zip(df.columns, row)) for row in df.values]
    return result

def filter_clinical_trials(df, column_name, search_term):
    if column_name and search_term:
        df = df[df[column_name].astype(str).str.contains(search_term, case=False, na=False)]
    df = df.dropna(axis=1, how='all')
    df = df.where(pd.notnull(df), None)
    result = [OrderedDict(zip(df.columns, row)) for row in df.values]
    return result
