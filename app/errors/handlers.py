# Importing necessary modules
from flask import render_template
from app import db
from app.errors import bp

# Error handler for 400 Bad Request error
@bp.app_errorhandler(400)
def bad_request(error):
    """Render a custom template for 400 Bad Request error."""
    return render_template('errors/400.html'), 400

# Error handler for 404 Not Found error
@bp.app_errorhandler(404)
def not_found_error(error):
    """Render a custom template for 404 Not Found error."""
    return render_template('errors/404.html'), 404

# Error handler for 500 Internal Server Error
@bp.app_errorhandler(500)
def internal_error(error):
    """Rollback the database session and render a custom template for 500 Internal Server Error."""
    db.session.rollback()
    return render_template('errors/500.html'), 500
