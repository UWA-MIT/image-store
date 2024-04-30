# Importing Flask Blueprint module
from flask import Blueprint

# Creating a Blueprint instance for the users module
bp = Blueprint('users', __name__)

# Import and register routes for user-related functionality
from app.users import routes
