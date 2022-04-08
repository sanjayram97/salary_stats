from flask import Flask, render_template, request, session, redirect, url_for
from fetch_preprocess_data import fetch_preprocess_data
from pay_stats_utils import salary_pos_title, salary_pos_company, salary_pos_location, salary_pos_company_title, get_mean_details, salary_title_chart
from fetch_preprocess_data import preprocess_string
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)

##### DB TABLE
class salaryreported(db.Model):
    # __tablename__ = 'repsalaries'
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.Text)
    title = db.Column(db.Text)
    location = db.Column(db.Text)
    salary = db.Column(db.Integer)

    def __init__(self, company, title, location, salary):
        self.company = company
        self.title = title
        self.location = location
        self.salary = salary

    def __repr__(self):
        return f"Company: {self.company}, Title: {self.title}, Location: {self.location}, Salary: {self.salary}"


##### Data
df, df_company_aggregates, df_job_title_aggregates = fetch_preprocess_data()
companies = df['Company Name_preprocessed'].sort_values().unique().tolist()
titles = df['Job Title_preprocessed'].sort_values().unique().tolist()
comp_title_df = df[['Company Name_preprocessed', 'Job Title_preprocessed', 'Location']]
print('completed data fetch and preprocess')
##### Data

##### Views
@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html', companies = companies, titles = titles, comp_title_df = comp_title_df)

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

    company_title_flag, pos, ppl_below_you, tot_ppl = salary_pos_company_title(salary, company+title, df)
    company_title_pos = {"company_title_flag": company_title_flag, "pos": round(pos*100), "ppl_below_you": int(ppl_below_you), "tot_ppl": int(tot_ppl)}
    # print('Company and Title: ', company_title_pos)

    plot_data = salary_title_chart(df, title)

    return render_template('outcome.html', 
                            title_pos = title_pos, 
                            company_pos = company_pos, 
                            location_pos = location_pos, 
                            company_title_pos = company_title_pos,
                            input_params = input_params,
                            avg_details = avg_details,
                            chart_data_labels = plot_data['range'].tolist(),
                            chart_data_values = plot_data['count'].tolist())


@app.route('/report_salary', methods=['POST','GET'])
def report_salary():
    return render_template('report_salary_temp.html')

@app.route('/thankyou', methods=['POST'])
def thankyou():
    company = request.form.get("company")
    title = request.form.get("title")
    location = request.form.get("location")
    salary = request.form.get("salary")
    record = salaryreported(company, title, location, int(salary))
    db.session.add(record)
    db.session.commit()

    return render_template('thankyou.html', company = company,
                            title = title,
                            location = location,
                            salary = salary)

import sqlite3
@app.route('/viewsal', methods=['POST','GET'])
def viewsal():
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    cur.execute("select * from salaryreported")
    rows = cur.fetchall()
    print(rows)
    conn.close()
    return str(rows)

if __name__ == "__main__":
    app.run(debug=False)