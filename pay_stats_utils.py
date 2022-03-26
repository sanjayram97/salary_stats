import pandas as pd
from csv import writer

def salary_pos_title(sal, title, df):
    ppl_below_you = df['Salaries Reported'][(df['Job Title_preprocessed'] == title) 
                                                & (df['Tot_sal'] <= sal)].sum()
    tot_ppl = df['Salaries Reported'][df['Job Title_preprocessed'] == title].sum()
    pos = ppl_below_you / tot_ppl
    return pos, ppl_below_you, tot_ppl

def salary_pos_company(sal, company, df):
    ppl_below_you = df['Salaries Reported'][(df['Company Name_preprocessed'] == company) 
                                                & (df['Tot_sal'] <= sal)].sum()
    tot_ppl = df['Salaries Reported'][df['Company Name_preprocessed'] == company].sum()
    pos = ppl_below_you / tot_ppl
    return pos, ppl_below_you, tot_ppl

def salary_pos_company_title(sal, company_title, df):
    if company_title not in df['Company_Title'].unique():
        return 0, 0, 0, 0
    ppl_below_you = df['Salaries Reported'][(df['Company_Title'] == company_title)
                                                & (df['Tot_sal'] <= sal)].sum()
    tot_ppl = df['Salaries Reported'][df['Company_Title'] == company_title].sum()
    
    pos = ppl_below_you / tot_ppl
    
    return 1, pos, ppl_below_you, tot_ppl

def salary_pos_location(sal, location, df):
    ppl_below_you = df['Salaries Reported'][(df['Location_preprocessed'] == location) 
                                                & (df['Tot_sal'] <= sal)].sum()
    tot_ppl = df['Salaries Reported'][df['Location_preprocessed'] == location].sum()
    pos = ppl_below_you / tot_ppl
    return pos, ppl_below_you, tot_ppl

def salary_pos_location_title(sal, location_title, df):
    ppl_below_you = df['Salaries Reported'][(df['Location_Title'] == location_title)
                                                & (df['Tot_sal'] <= sal)].sum()
    tot_ppl = df['Salaries Reported'][df['Location_Title'] == location_title].sum()
    pos = ppl_below_you / tot_ppl
    return pos, ppl_below_you, tot_ppl

def get_mean_details(input_params, df):

    company_avg_sal = round(df['Tot_sal_sum'][df['Company Name_preprocessed'] == input_params['company']].sum() / df['Salaries Reported'][df['Company Name_preprocessed'] == input_params['company']].sum())
    title_avg_sal = round(df['Tot_sal_sum'][df['Job Title_preprocessed'] == input_params['title']].sum() / df['Salaries Reported'][df['Job Title_preprocessed'] == input_params['title']].sum())
    location_avg_sal = round(df['Tot_sal_sum'][df['Location_preprocessed'] == input_params['location']].sum() / df['Salaries Reported'][df['Location_preprocessed'] == input_params['location']].sum())

    if input_params['location']+input_params['title'] in df['Location_Title'].unique():
        location_title_avg_sal = round(df['Tot_sal_sum'][df['Location_Title'] == input_params['location']+input_params['title']].sum() / df['Salaries Reported'][df['Location_Title'] == input_params['location']+input_params['title']].sum())
        location_title_avg_sal/= 100000
        location_title_avg_sal = str(round(location_title_avg_sal, 1)) + ' LPA'
    else:
        location_title_avg_sal = False

    company_avg_sal/= 100000
    title_avg_sal/= 100000
    location_avg_sal/= 100000
    

    company_avg_sal = str(round(company_avg_sal, 1)) + ' LPA'
    title_avg_sal = str(round(title_avg_sal, 1)) + ' LPA'
    location_avg_sal = str(round(location_avg_sal, 1)) + ' LPA'

    mean_details = {"company_avg": company_avg_sal,
                    "title_avg": title_avg_sal, 
                    "location_avg": location_avg_sal, 
                    "location_title_avg": location_title_avg_sal}

    print('Average details: ', mean_details)
    
    return mean_details

def insert_record(details):
    with open('data/new_records.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(details)
        f_object.close()