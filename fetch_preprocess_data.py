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

def salary_range(x):
    if x<=3:
        return 0
    elif x>3 and x<=5:
        return 1
    elif x>5 and x<=7:
        return 2
    elif x>7 and x<=10:
        return 3
    elif x>10 and x<=12:
        return 4
    elif x>12 and x<=14:
        return 5
    elif x>14 and x<=16:
        return 6
    elif x>16 and x<=18:
        return 7
    elif x>18 and x<=20:
        return 8
    elif x>20 and x<=22:
        return 9
    elif x>22 and x<=24:
        return 10
    elif x>24 and x<=26:
        return 11
    elif x>26 and x<=28:
        return 12
    elif x>28 and x<=30:
        return 13
    elif x>30 and x<=32:
        return 14
    elif x>32 and x<=34:
        return 15
    elif x>34 and x<=36:
        return 16
    elif x>36 and x<=38:
        return 17
    elif x>38 and x<=40:
        return 18
    else:
        return 19

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

    df['Tot_sal_in_lacs'] = df['Tot_sal'] / 100000
    df['Tot_sal_in_lacs'] = round(df['Tot_sal_in_lacs'])
    df['salary_range'] = df['Tot_sal_in_lacs'].apply(salary_range)

    print('Aggregating by company')
    df_company_aggregates = df.groupby(['Company Name']).agg({'Tot_sal': ['mean', 'median', 'count']}).reset_index()
    df_company_aggregates.columns = ['Company Name', 'mean', 'median', 'count']

    print('Aggregating by title')
    df_job_title_aggregates = df.groupby(['Job Title']).agg({'Tot_sal': ['mean', 'median', 'count']}).reset_index()
    df_job_title_aggregates.columns = ['Job Title', 'mean', 'median', 'count']
    print('Data exercise completed')
    
    return df, df_company_aggregates, df_job_title_aggregates