from flask import Flask, request, render_template, flash


app=Flask(__name__, template_folder='templates')

@app.route('/')
def p1():
    return render_template('landingpage.html')

db={"":""}

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
    
@app.route('/login',methods=["POST"])
def login():
    # Recieving details of the camp logging in
    email=request.form["Email"]
    password=request.form["password"]

    if email not in db and email!="":
        return render_template('login.html',info="Invalid username")
    elif db[email]!=password and password!="":
        return render_template('login.html',info="Invalid password")
    elif db[email]==password:
        return render_template('home.html')
    else:
        return
    
    

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
    app.run()