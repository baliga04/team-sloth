# 9 total endpoints
from app.admin_endpoints import bp
from app.extensions import db, validate_password

from flask import jsonify, request

from app.models.user import User
from app.models.budgets import Budgets

@bp.route('/create_user/', methods=['POST'])
def create_user():
    pass