    Loan Approval Expert System
This is a Flask-based web application designed to serve as an intelligent system for determining loan eligibility. Users can sign up, submit personal and financial information, and receive a decision on their loan application based on pre-defined data and rules.

    Features
~ User registration and login system with session management

~ Step-by-step form collection for personal and financial information

~ Intelligent decision-making using a rule-based engine with a CSV dataset

~ Loan interest and repayment calculations based on duration

~ SQLite database to store user accounts and loan decisions

~ User-friendly result page summarizing the loan decision and repayment details

    How It Works
**User Signup/Login: Users register and log in to access the loan application.

**Information Collection: The system gathers:

~ Personal Info (name, age, address, etc.)

~ Employment and Financial Details

~ Credit Score and Loan Preferences

** Loan Evaluation:

~ Uses rules from a CSV file (bank.csv) to compare user data against minimum thresholds.

~ Calculates interest based on the repayment duration.

~ Returns a decision (approve or decline), displayed in a styled HTML summary.

**Data Persistence: All user info and decisions are stored in the database for potential audit/logging.

    Setup Instructions
**Prerequisites
~ Python 3.7+
~ pip installed

**Installation
~ Clone this repository Using the following code:

git clone https://github.com/yourusername/loan-approval-expert-system.git

cd loan-approval-expert-system

~Create a virtual environment and activate it using the following code:


python -m venv venv #To create the virtual environment

On Mac and linux:
source venv/bin/activate #To activate it   

On Windows: 
venv\Scripts\activate #To ativate

~ Install dependencies:


pip install -r requirements.txt

~ Add your dataset:

Place your bank.csv file in the root directory. It should contain columns:

credit_score, income, debt, decision

~ Run the application:

python app.py
 Then visit http://127.0.0.1:5000/ in your browser.
