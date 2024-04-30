# Importing necessary modules
from flask import render_template
from datetime import datetime, timezone
from flask_login import current_user

from app import db
from app.main import bp
from app.models.user import user_count
from app.models.product import image_count
from app.models.reward import Reward
from app.models.product import Product

# Update the last_seen attribute of the current user's model before processing each request
@bp.before_request
def before_request():
    """Update the last_seen attribute of the current user's model before processing each request."""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

# Route for the main index page
@bp.route('/')
@bp.route('/index')
def index():
    """
    Render the main index page with recent images, user count, image count, and total credit rewards.

    Returns:
        str: Rendered HTML template with recent images, user count, image count, and total credit rewards.
    """
    recent_images = Product.query.filter_by().order_by(Product.timestamp.desc()).limit(12).all()
    return render_template('main/index.html', user_count=user_count(), image_count=image_count(), recent_images=recent_images, total_credit_rewards=Reward.total_credit_rewards())
