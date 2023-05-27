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


    
@app.route('/login',methods=["POST"])
def login():
    # Recieving details of the camp logging in
    email=request.form["Email"]
    password=request.form["password"]

    # Checking if the user exists
    user = User.query.filter_by(Email=email).first()
    if user is None:
        return flash("Invalid user")

    # Checking if the password matches
    elif not bcrypt.check_password_hash(user.password,password):
        return flash("Invalid password")
    
    else:
        return render_template('home.html')
    
    

@app.route('/create_user/', methods=['POST'])
def create_user():
    user_details=request.get_json()
    email=user_details.get("email")
    password=user_details.get("password")
    first_name=user_details.get("first_name")
    last_name=user_details.get("last_name")
    confirm_password=user_details.get("confirm_password")

    if User.query.filter_by(Email=email.strip()).first() is not None:
        return flash("User already exists")
    
    #empty fields
    if not email and not email.strip():
        return flash("error Email has to be entered")
    elif not first_name and not first_name.strip():
        return flash("error First name has to be entered")
    elif not password and not password.strip():
        return flash("error Password has to be entered")
    
    #validating password
    if not password.strip():
         return flash("error Passwords cannot be empty")
    if password != confirm_password:
        return flash("error Passwords not matching")
    if not validate_password(password): 
        return flash("error Invaid password pattern.")
    
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

    return render_template('registration.html')

if __name__=='__main__':
    app.run(debug=True)