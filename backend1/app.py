from flask import Flask, request, render_template, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import os
import re
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__, template_folder='templates')

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

bcrypt = Bcrypt(app)
# server_session=Session(app)
db = SQLAlchemy(app)

class Budgets(db.Model):
    UserID: int = db.Column(db.Integer, db.ForeignKey('user.UserID'), primary_key=True)
    Category: str = db.Column(db.String(50), primary_key=True)
    Budget: float = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
         return f'<Budget>'
    
class User(db.Model):
    UserID: int = db.Column(db.Integer, primary_key=True)
    FirstName: str = db.Column(db.String(50), nullable=False)
    LastName: str = db.Column(db.String(50), nullable=False)
    Email: str = db.Column(db.String(50), nullable=False)
    Password: str = db.Column(db.Text, nullable=False)
    Balance: float = db.Column(db.Float, nullable=False,default=0.0)

    # On Delete Cascade
    transactions = relationship("Transactions", backref="User",cascade="all, delete-orphan") 

    def __repr__(self):
         return f'<User>'
    
class Transactions(db.Model):
    TransactionID: int = db.Column(db.Integer, primary_key=True)
    UserID: int = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    Amount: float = db.Column(db.Float, nullable=False)
    Category: str = db.Column(db.String(50), nullable=False)
    DateTime: str = db.Column(db.DateTime(timezone=True), nullable=False)
    Description: str = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
         return f'<Transactions>'
    
with app.app_context():
    db.create_all()


# Flask Bcrypt
bcrypt = Bcrypt()

# Validate Password


def validate_password(password):

    # Password checker
    # Primary conditions for password validation:
    # Minimum 8 characters.
    # The alphabet must be between [a-z]
    # At least one alphabet should be of Upper Case [A-Z]
    # At least 1 number or digit between [0-9].
    # At least 1 character from [ _ or @ or $ ]. 

    #\s- Returns a match where the string contains a white space character
    if len(password) < 8 or re.search("\s" , password):  
        return False  
    if not (re.search("[a-z]", password) and re.search("[A-Z]", password) and re.search("[0-9]", password) ):
        return False  
    return True  

@app.route('/')
def p1():
    return render_template('landingpage.html')

@app.route('/form_login')
def form_login():
    return render_template('login.html')

@app.route('/form_registration')
def form_registration():
    return render_template('registration.html')
    
@app.route('/login',methods=["POST"])
def login():
    # Recieving details of the camp logging in
    email=request.form["email"]
    password=request.form["password"]

    # Checking if the user exists
    user = User.query.filter_by(Email=email).first()
    if user is None:
        flash("Invalid username/password")
        return redirect(url_for('form_login'))

    # Checking if the password matches
    elif not bcrypt.check_password_hash(user.Password,password):
        flash("Invalid username/password")
        return redirect(url_for('form_login'))
    
    else:
        return render_template('home.html')
    
    

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('registration.html')

    email=request.form["email"]
    password=request.form["password"]
    first_name=request.form["first_name"]
    last_name=request.form["last_name"]
    confirm_password=request.form["confirm_password"]

    if User.query.filter_by(Email=email.strip()).first() is not None:
        return flash("User already exists")
    
    # Checking for empty fields
    if not email and not email.strip():
        flash("Error: Email is mandatory")
        return redirect(url_for('register'))
    elif not first_name and not first_name.strip():
        flash("Error: First name is mandatory")
        return redirect(url_for('register'))
    elif not password and not password.strip():
        flash("Error: Password is mandatory")
        return redirect(url_for('register'))
    elif not confirm_password and not confirm_password.strip():
        flash("Error: Confirm password is mandatory")
        return redirect(url_for('register'))
    elif password != confirm_password:
        flash("Error: Passwords do not match")
        return redirect(url_for('register'))
    
    
    #validating password
    if not password.strip():
        flash("Error: Passwords cannot be empty")
        return redirect(url_for('register'))
    if not validate_password(password): 
        flash("Error: Invaid password pattern.")
        return redirect(url_for('register'))
    
    # Hashing the password
    hashed_password=bcrypt.generate_password_hash(password)

    #add user to database
    new_user =User( FirstName=first_name,
                    Password=hashed_password,
                    LastName=last_name,
                    Email=email,
                )
    db.session.add(new_user)
    db.session.commit()

    return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True)