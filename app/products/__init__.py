# Importing Flask Blueprint module
from flask import Blueprint

# Creating a Blueprint instance for the products module
bp = Blueprint('products', __name__)

# Importing routes from the products module
from app.products import routes