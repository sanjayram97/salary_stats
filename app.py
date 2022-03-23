from flask import Flask, render_template, request, session, redirect, url_for
from fetch_preprocess_data import fetch_preprocess_data
from pay_stats_utils import salary_pos_title, salary_pos_company, salary_pos_location, salary_pos_company_title
from fetch_preprocess_data import preprocess_string
from utils import get_mean_details, insert_record

app = Flask(__name__)

df, df_company_aggregates, df_job_title_aggregates = fetch_preprocess_data()
companies = df['Company Name_preprocessed'].sort_values().unique().tolist()
titles = df['Job Title_preprocessed'].sort_values().unique().tolist()
print('completed data fetch and preprocess')

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html', companies = companies, titles = titles)

@app.route('/func', methods=['POST'])
def func():
    company = request.form.get("company")
    title = request.form.get("title")
    print(company)
    print(title)
    location = request.form.get("location")
    salary = int(request.form.get("salary"))
    print(df[['Job Title', 'Job Title_preprocessed']].head(2))

    input_params = {"company": company, "title": title, "location": location, "salary": salary}

    # company = preprocess_string(company)
    # title = preprocess_string(title)
    location = preprocess_string(location)

    preprocessed_input_params = {"company": company, "title": title, "location": location, "salary": salary}
    avg_details = get_mean_details(preprocessed_input_params, df)

    pos, ppl_below_you, tot_ppl = salary_pos_title(salary, title, df)
    title_pos = {"pos": round(pos*100), "ppl_below_you": int(ppl_below_you), "tot_ppl": int(tot_ppl)}
    # print('Title: ', title_pos)
    
    pos, ppl_below_you, tot_ppl = salary_pos_company(salary, company, df)
    company_pos = {"pos": round(pos*100), "ppl_below_you": int(ppl_below_you), "tot_ppl": int(tot_ppl)}
    # print('Company: ', company_pos)

    pos, ppl_below_you, tot_ppl = salary_pos_location(salary, location, df)
    location_pos = {"pos": round(pos*100), "ppl_below_you": int(ppl_below_you), "tot_ppl": int(tot_ppl)}
    # print('Location: ', location_pos)

    pos, ppl_below_you, tot_ppl = salary_pos_company_title(salary, company+title, df)
    company_title_pos = {"pos": round(pos*100), "ppl_below_you": int(ppl_below_you), "tot_ppl": int(tot_ppl)}
    # print('Company and Title: ', company_title_pos)

    return render_template('outcome.html', 
                            title_pos = title_pos, 
                            company_pos = company_pos, 
                            location_pos = location_pos, 
                            company_title_pos = company_title_pos,
                            input_params = input_params,
                            avg_details = avg_details)


@app.route('/report_salary', methods=['POST','GET'])
def report_salary():
    return render_template('report_salary_temp.html')

@app.route('/thankyou', methods=['POST'])
def thankyou():
    company = request.form.get("company")
    title = request.form.get("title")
    location = request.form.get("location")
    salary = request.form.get("salary")
    insert_record([company, title, location, salary])
    return render_template('thankyou.html', company = company,
                            title = title,
                            location = location,
                            salary = salary)


if __name__ == "__main__":
    app.run(debug=True)