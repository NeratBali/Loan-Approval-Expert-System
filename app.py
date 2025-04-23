from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
#from Agah
from datetime import datetime
import pandas as pd  # type: ignore

app = Flask(__name__)
app.secret_key = 'your_secret_key'
#From Agah
def decide_loan():
    try:
        return pd.read_csv('bank.csv')
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()

# Store user data temporarily
user_data = {}
# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loan_approval_expert_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# SQLAlchemy model for the User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.firstName} {self.lastName}>"
    
class LoanDecision(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    credit_score = db.Column(db.Integer, nullable=False)
    income = db.Column(db.Float, nullable=False)
    debt = db.Column(db.Float, nullable=False)
    decision = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        return f"<LoanDecision {self.id} - {self.decision}>"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        new_user = User(firstName=firstName, lastName=lastName, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Return success with redirect instruction
        return jsonify({
            'success': True,
            'message': 'User signed up successfully!',
            'redirect': url_for('index')  # Will show login modal
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 400
@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            session['first_name'] = user.firstName
            session['last_name'] = user.lastName
            return redirect(url_for('collection_of_information'))  # Use route name, not template name
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/collection_of_information')
def collection_of_information():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('collection_of_information.html',  first_name=session.get('first_name', ''),last_name=session.get('last_name', ''))

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
        decision = "decline"
    else:
        decision = 'decline'
        for index, row in loan_data.iterrows():
            try:
                row_credit_score = int(row['credit_score'])
                row_income = float(row['income'])
                row_debt = float(row['debt'])
            except (ValueError, TypeError, KeyError):
                continue

            print(f"Row {index}: score>={row_credit_score}, income>={row_income}, debt<={row_debt}")

            if credit_score >= row_credit_score and income >= row_income and debt <= row_debt:
                decision = row.get('decision', 'decline')
                break

    # Save the decision to the database
    loan_decision = LoanDecision(
        credit_score=credit_score,
        income=income,
        debt=debt,
        decision=decision
    )
    db.session.add(loan_decision)
    db.session.commit()

    return decision

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)