import pandas as pd

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
    ppl_below_you = df['Salaries Reported'][(df['Company_Title'] == company_title)
                                                & (df['Tot_sal'] <= sal)].sum()
    tot_ppl = df['Salaries Reported'][df['Company_Title'] == company_title].sum()
    
    pos = ppl_below_you / tot_ppl
    
    return pos, ppl_below_you, tot_ppl

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