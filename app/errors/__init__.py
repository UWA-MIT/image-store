# Importing Blueprint from Flask
from flask import Blueprint

# Creating a Blueprint instance for handling errors
bp = Blueprint('errors', __name__)

# Importing error handlers to be registered with this Blueprint
from app.errors import handlers
