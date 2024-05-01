# Importing Flask Blueprint module
from flask import Blueprint

# Creating a Blueprint instance for the main module
bp = Blueprint('main', __name__)

# Importing routes from the main module
from app.main import routes