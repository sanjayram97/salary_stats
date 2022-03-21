import pandas as pd
import numpy as np
import re

# Utils
def split_sal_freq(x):
    curr = x[0]
    sal = int(x[1:].split('/')[0].replace(',',''))
    freq = x[1:].split('/')[1]
    return pd.Series([curr, sal, freq])

def get_monthly_sal(x):
    if x['freq'] == 'hr':
        return x['Sal'] * 24 * 30 * 12
    elif x['freq'] == 'mo':
        return x['Sal'] * 12
    else:
        return x['Sal']
    
def preprocess_string(x):
    x = x.lower()
    x = re.sub(r'[^\w\s]', '', x)
    x = x.replace(' ','')
    return x

def fetch_preprocess_data():
    # input dataset
    print('Reading dataset')
    df = pd.read_csv('data/Salary Dataset.csv')
    df['Salaries Reported'] = df['Salaries Reported'].fillna(1)
    df['Currency'] = df['Salary'].apply(lambda x: x[0])
    df = df[df['Currency']=='₹']
    df[['Currency','Sal','freq']] = df['Salary'].apply(split_sal_freq)
    df['Tot_sal'] = df[['Sal','freq']].apply(lambda x: get_monthly_sal(x), axis=1)

    ##### preprocess string
    print('Preprocessing data')
    df['Company Name'] = df['Company Name'].astype(str)
    df['Job Title'] = df['Job Title'].astype(str)
    df['Location'] = df['Location'].astype(str)

    df['Company Name_preprocessed'] = df['Company Name'].apply(lambda x: preprocess_string(x))
    df['Job Title_preprocessed'] = df['Job Title'].apply(lambda x: preprocess_string(x))
    df['Location_preprocessed'] = df['Location'].apply(lambda x: preprocess_string(x))
    
    # Refactored job title
    df_title = pd.read_csv('data/title_map.csv')
    df_title_1 = df_title[['Job Title_preprocessed', 'title_map_1']]
    df_title_1 = df_title_1.dropna()
    df_title_2 = df_title[['Job Title_preprocessed', 'title_map_2']]
    df_title_2 = df_title_2.dropna()

    title_map_1 = df_title_1.set_index('Job Title_preprocessed').to_dict()['title_map_1']
    title_map_2 = df_title_2.set_index('Job Title_preprocessed').to_dict()['title_map_2']

    df_1 = df.copy()
    df_2 = df.copy()

    df_1['Job Title_preprocessed'] = df_1['Job Title_preprocessed'].map(title_map_1)
    df_2['Job Title_preprocessed'] = df_2['Job Title_preprocessed'].map(title_map_2)

    df = df_1.append(df_2, ignore_index=True)
    df = df.dropna()
    
    # Refactored company name
    df_company = pd.read_csv('data/company_map.csv')
    df_company = df_company[['Company Name_preprocessed', 'company_map']]
    df_company = df_company.dropna()
    df_company = df_company.set_index('Company Name_preprocessed')
    company_map = df_company.to_dict()['company_map']

    df['Company Name_preprocessed'] = df['Company Name_preprocessed'].map(company_map)
    df = df.dropna()
    
    # Total sum of salary = Tot_sal * Salaries reported
    df['Tot_sal_sum'] = df['Tot_sal'] * df['Salaries Reported']

    # Multiple aggregates
    
    df['Company_Title'] = df['Company Name_preprocessed'] + df['Job Title_preprocessed']
    df['Location_Title'] = df['Location_preprocessed'] + df['Job Title_preprocessed']


    ##### remove invalid companies and titles
    print('Removing invalid companies and titles')
    invalid_companies = ['---']
    invalid_job_title = []
    df = df[~df['Company Name'].isin(invalid_companies)]
    df = df[~df['Job Title'].isin(invalid_job_title)]

    print(' --------------------------------- ')
    print('Total number of salaries reported  : ', sum(df['Salaries Reported']))
    print('Total number of companies          : ', df['Company Name'].nunique())
    print('Total number of job titles         : ', df['Job Title'].nunique())
    print('Total number of locations          : ', df['Location'].nunique())
    print(' --------------------------------- ')

    print('Aggregating by company')
    df_company_aggregates = df.groupby(['Company Name']).agg({'Tot_sal': ['mean', 'median', 'count']}).reset_index()
    df_company_aggregates.columns = ['Company Name', 'mean', 'median', 'count']

    print('Aggregating by title')
    df_job_title_aggregates = df.groupby(['Job Title']).agg({'Tot_sal': ['mean', 'median', 'count']}).reset_index()
    df_job_title_aggregates.columns = ['Job Title', 'mean', 'median', 'count']
    print('Data exercise completed')
    
    return df, df_company_aggregates, df_job_title_aggregates