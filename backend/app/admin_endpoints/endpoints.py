# 9 total endpoints
from app.admin_endpoints import bp
from app.extensions import db, validate_password, bcrypt

from flask import jsonify, request

from app.models.user import User
from app.models.budgets import Budgets

@bp.route('/create_user/', methods=['POST'])
def create_user():
    user_details=request.get_json()
    email=user_details.get("email")
    password=user_details.get("password")
    first_name=user_details.get("first name")
    last_name=user_details.get("last name")
    confirm_password=user_details.get("confirm password")

    if User.query.filter_by(Email=email.strip()).first() is not None:
        return jsonify({"error":"User already exists"})
    
    #empty fields
    if not email and not email.strip():
        return jsonify({"error":"Email has to be entered"})
    elif not first_name and not first_name.strip():
        return jsonify({"error":"First name has to be entered"})
    elif not password and not password.strip():
        return jsonify({"error":"Password has to be entered"})
    
    #validating password
    if not password.strip():
         return jsonify({"error": "Passwords cannot be empty"})
    if password != confirm_password:
        return jsonify({"error": "Passwords not matching"})
    if not validate_password(password): 
        return jsonify({"error": "Invaid password pattern."})
    
    # Hashing the password
    hashed_password=bcrypt.generate_password_hash(password)

    #add user to database
    new=User( FirstName=first_name,
              Password=password,
              LastName=last_name,
              Email=email,
            )
    db.session.add(new)
    db.session.commit()