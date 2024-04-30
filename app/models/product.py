# Importing necessary modules
from datetime import datetime, timezone
from flask import current_app
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from openai import OpenAI
import requests
import uuid
import time
import os

# Define the base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Product model class
class Product(db.Model):
    # Database columns
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(60))
    image = sa.Column(sa.String(256))
    category = sa.Column(sa.String(50))
    price = sa.Column(sa.Float(precision=2))
    timestamp = sa.Column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    
    is_sold = sa.Column(sa.Boolean(), default=False)
    sold_at = sa.Column(sa.DateTime, default=None, nullable=True)

    seller_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), index=True)
    buyer_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), index=True, default=None, nullable=True)

    # Relationship with User model
    seller = so.relationship('User', foreign_keys=[seller_id], backref='products_selling')

    # Method to generate an image based on the category using OpenAI
    def generate_image(self, name, category):

        client = OpenAI(
            api_key=current_app.config['OPENAI_API_KEY']
        )
        response = client.images.generate(
            model="dall-e-2",
            prompt=category + ": " + name,
            n=1,
            size="256x256"
        )

        try:
            url = response.data[0].url
            if self.check_url_exists(url):
                return self.download_and_save_image(url)
        except Exception as e:
            print(e)
            pass

        return None

    # Method to check if a URL exists
    def check_url_exists(self, url):
        try:
            r = requests.head(url, timeout=5)
            if r.status_code in range(200, 299):
                return True
            else:
                return False
        except requests.ConnectionError:
            return False
        except requests.RequestException as e:
            return False

    # Method to download and save an image
    def download_and_save_image(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                filename = f"{int(time.time())}_{uuid.uuid4().hex}.png"
                path = os.path.join(basedir, '../static/images/nft/' + filename)
                with open(path, 'wb') as f:
                    f.write(response.content)
                return filename
        except Exception as e:
            print(e)
            return None

# Function to get the count of images
def image_count():
    return Product.query.count()
