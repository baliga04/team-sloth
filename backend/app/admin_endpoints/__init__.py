from flask import Blueprint

# Creating a Blueprint
bp = Blueprint('admin_endpoints', __name__)

# Importing the endpoints
from app.admin_endpoints import endpoints