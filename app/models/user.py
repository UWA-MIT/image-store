from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import jwt

from datetime import datetime, timezone
from time import time
import sqlalchemy as sa
from flask import current_app
from app import db
from app import login
from app.models import product

class User(UserMixin, db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(64), index=True, unique=True)
    name = sa.Column(sa.String(64), index=False)
    email = sa.Column(sa.String(120), index=True, unique=True)
    password_hash = sa.Column(sa.String(256))
    status = sa.Column(sa.String(20), index=True)
    about_me = sa.Column(sa.String(140))
    money = sa.Column(sa.Integer(), default=100)
    last_seen = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, id)
    

    def get_image_count(self, user_id):

        image_count = product.Product.query.filter_by(seller_id=user_id).count()
        
        return image_count

    def get_purchase_count(self, user_id):
        purchase_count = product.Product.query.filter_by(buyer_id=user_id).count()
        return purchase_count


def user_count():
    return User.query.count()





