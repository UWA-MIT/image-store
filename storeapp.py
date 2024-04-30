import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db

# Create the Flask application
app = create_app()

# Define a shell context processor to make certain objects available in the Flask shell
@app.shell_context_processor
def make_shell_context():
    """
    Defines the context for the Flask shell.

    Returns:
        dict: A dictionary containing objects to be available in the Flask shell.
    """
    return {'sa': sa, 'so': so, 'db': db}