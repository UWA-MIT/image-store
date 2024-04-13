from flask import render_template
from datetime import datetime, timezone
from flask_login import current_user

from app import db
from app.main import bp
from app.models.user import user_count
from app.models.product import image_count


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/index.html', user_count=user_count(), image_count=image_count())




