from flask import Flask, render_template, request, redirect, url_for  # type: ignore
from datetime import datetime
import pandas as pd  # type: ignore

app = Flask(__name__)

def decide_loan():
    try:
        return pd.read_csv('bank.csv')
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()

# Store user data temporarily
user_data = {}

@app.route('/')
def collection_of_information():
    return render_template('collection_of_information.html')

@app.route('/financial_records', methods=['POST'])
def financial_records():
    user_data['first_name'] = request.form.get('first_name')
    user_data['last_name'] = request.form.get('last_name')
    user_data['age_range'] = request.form.get('age_range')
    user_data['address'] = request.form.get('address')
    user_data['state'] = request.form.get('state')
    user_data['next_of_kin'] = request.form.get('next_of_kin')
    user_data['occupation'] = request.form.get('occupation')
    return render_template('financial_records.html')

@app.route('/loan_application', methods=['POST'])
def loan_application():
    user_data['working'] = request.form.get('working')
    user_data['salary'] = request.form.get('salary')
    user_data['other_income'] = request.form.get('other_income')
    user_data['other_income_amount'] = request.form.get('other_income_amount')
    
    debt_value = request.form.get('debt', '').strip().lower()
    try:
        user_data['debt'] = float(debt_value) if debt_value not in ['no', 'none', ''] else 0.0
    except ValueError:
        user_data['debt'] = 0.0

    user_data['repay_plan'] = request.form.get('repay_plan')
    user_data['credit_history'] = request.form.get('credit_history')

    credit_score_range = request.form.get('credit_score')
    credit_score = int(credit_score_range.split('-')[0]) if credit_score_range else 0
    user_data['credit_score'] = credit_score

    user_data['agreement'] = request.form.get('agreement')

    loan_amount_raw = request.form.get('loan_amount', 0).replace(',', '')
    user_data['loan_amount'] = float(loan_amount_raw)

    return render_template('loan_application_form.html')

@app.route('/calculate_loan', methods=['POST'])
def calculate_loan():
    try:
        # Get loan amount from the form, ensuring no commas and convert to float
        loan_amount_raw = request.form.get('loan_amount', '0').replace(',', '')
        loan_amount = float(loan_amount_raw)

        # Get the payback date and calculate loan duration in months
        payback_date_str = request.form.get('loan_duration')
        payback_date = datetime.strptime(payback_date_str, '%Y-%m-%d')
        today = datetime.today()

        # Calculate difference in months
        months_diff = (payback_date.year - today.year) * 12 + (payback_date.month - today.month)
        if payback_date.day > today.day:
            months_diff += 1
        loan_duration = max(1, months_diff)

        # Calculate interest based on loan duration
        if loan_duration == 1:
            interest_rate = 0.05
        elif loan_duration == 2:
            interest_rate = 0.10
        else:
            interest_rate = 0.05 * loan_duration

        # Calculate total repayable amount
        total_amount = loan_amount + (loan_amount * interest_rate)

        # Save these values to user_data
        user_data['loan_amount'] = loan_amount
        user_data['loan_duration'] = loan_duration

        # Make loan decision
        decision = make_loan_decision(user_data)

        # Log the values for debugging purposes
        print(f"Loan Amount: {loan_amount}, Duration: {loan_duration}, Decision: {decision}")

        # Return the result as rendered HTML
        return render_template(
            'loan_result.html',
            loan_amount=loan_amount,
            duration=loan_duration,
            total_amount=total_amount,
            decision=decision
        )

    except Exception as e:
        # Catch any errors and display them
        return f"An error occurred: {e}"

def make_loan_decision(user_data):
    try:
        loan_data = decide_loan()
    except Exception as e:
        return f"Error loading dataset: {e}"

    try:
        credit_score = int(user_data.get('credit_score', 0))
    except ValueError:
        score_str = user_data.get('credit_score', '0')
        credit_score = int(score_str.split('-')[0])

    try:
        income = float(str(user_data.get('salary', '0')).replace(',', '')) + \
                 float(str(user_data.get('other_income_amount', '0')).replace(',', ''))
    except ValueError:
        income = 0.0

    try:
        debt = float(str(user_data.get('debt', '0')).replace(',', ''))
    except ValueError:
        debt = 0.0

    print(f"Evaluating Decision -> Credit Score: {credit_score}, Income: {income}, Debt: {debt}")

    if 300 <= credit_score <= 600:
        print("Declined due to low credit score.")
        return "decline"

    for index, row in loan_data.iterrows():
        try:
            row_credit_score = int(row['credit_score'])
            row_income = float(row['income'])
            row_debt = float(row['debt'])
        except (ValueError, TypeError, KeyError):
            continue

        print(f"Row {index}: score>={row_credit_score}, income>={row_income}, debt<={row_debt}")

        if credit_score >= row_credit_score and income >= row_income and debt <= row_debt:
            return row.get('decision', 'decline')

    return 'decline'

if __name__ == '__main__':
    app.run(debug=True)
