from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        # Extract form data
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']

        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'Email already registered'}), 400

        # Add the new user to the database
        new_user = User(firstName=firstName, lastName=lastName, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'User signed up successfully!'})
    except Exception as e:
        print(f"Error: {e}")  # Debug: Print the error
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    try:
        # Extract form data
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the database
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return jsonify({'success': True, 'message': 'Login successful!'})

        # If no match is found
        return jsonify({'success': False, 'message': 'Account does not exist'}), 400
    except Exception as e:
        print(f"Error: {e}")  # Debug: Print the error
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)