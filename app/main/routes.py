
from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from datetime import datetime, timezone
from flask_login import current_user, login_required

import sqlalchemy as sa
from app import db
from app.main import bp

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('main/index.html', title='Home', user=user, posts=posts)




