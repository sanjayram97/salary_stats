from numerize import numerize

def get_mean_details(input_params, df):

    company_avg_sal = round(df['Tot_sal_sum'][df['Company Name_preprocessed'] == input_params['company']].sum() / df['Salaries Reported'][df['Company Name_preprocessed'] == input_params['company']].sum())
    title_avg_sal = round(df['Tot_sal_sum'][df['Job Title_preprocessed'] == input_params['title']].sum() / df['Salaries Reported'][df['Job Title_preprocessed'] == input_params['title']].sum())
    location_avg_sal = round(df['Tot_sal_sum'][df['Location_preprocessed'] == input_params['location']].sum() / df['Salaries Reported'][df['Location_preprocessed'] == input_params['location']].sum())
    location_title_avg_sal = round(df['Tot_sal_sum'][df['Location_Title'] == input_params['location']+input_params['title']].sum() / df['Salaries Reported'][df['Location_Title'] == input_params['location']+input_params['title']].sum())

    # company_avg_sal = numerize.numerize(company_avg_sal)
    # title_avg_sal = numerize.numerize(title_avg_sal)
    # location_avg_sal = numerize.numerize(location_avg_sal)
    # location_title_avg_sal = numerize.numerize(location_title_avg_sal)

    company_avg_sal/= 100000
    title_avg_sal/= 100000
    location_avg_sal/= 100000
    location_title_avg_sal/= 100000

    company_avg_sal = str(round(company_avg_sal, 1)) + ' LPA'
    title_avg_sal = str(round(title_avg_sal, 1)) + ' LPA'
    location_avg_sal = str(round(location_avg_sal, 1)) + ' LPA'
    location_title_avg_sal = str(round(location_title_avg_sal, 1)) + ' LPA'

    mean_details = {"company_avg": company_avg_sal,
                    "title_avg": title_avg_sal, 
                    "location_avg": location_avg_sal, 
                    "location_title_avg": location_title_avg_sal}

    print('Average details: ', mean_details)
    
    return mean_details