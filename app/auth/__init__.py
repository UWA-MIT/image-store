from flask import Blueprint

# Create a Blueprint instance for authentication
bp = Blueprint('auth', __name__)

# Import routes module to register routes with the Blueprint instance
from app.auth import routes
