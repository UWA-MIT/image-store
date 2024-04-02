from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Product(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(60))
    image = sa.Column(sa.String(100))
    description = sa.Column(sa.String(256))
    price = sa.Column(sa.Float(precision=2))  # Changed to Float, and corrected the precision syntax
    timestamp = sa.Column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    
    is_sold = sa.Column(sa.Boolean(), default=False)
    sold_at = sa.Column(sa.DateTime, default=None, nullable=True)

    seller_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), index=True)
    buyer_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), index=True, default=None, nullable=True)


    # Define the seller relationship
    seller = so.relationship('User', foreign_keys=[seller_id], backref='products_selling')
    
    # Define the buyer relationship
    buyer = so.relationship('User', foreign_keys=[buyer_id], backref='products_bought')


    def __repr__(self):
        return '<Product {}>'.format(self.title)


    def generate_image(name):

        return None

        # import json
        # import requests

        # headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMDY2MzZhOWItYjA1ZS00NTZkLWIyNmEtMjFlYzA0YWE4M2Q3IiwidHlwZSI6ImFwaV90b2tlbiJ9.A5la8tV6HTwPgROS8WHNZReNjMSLpF3PEh7SGZZaT74"}

        # url = "https://api.edenai.run/v2/image/generation"
        # payload = {
        #     "providers": "openai",
        #     "text": "this is a test of Eden AI",
        #     "resolution": "512x512",
        #     "fallback_providers": ""
        # }

        # response = requests.post(url, json=payload, headers=headers)
        # result = json.loads(response.text)
        # print(result['openai']['items'])


        from openai import OpenAI
        client = OpenAI()

        response = client.images.generate(
          model="dall-e-3",
          prompt="a white siamese cat",
          size="1024x1024",
          quality="standard",
          n=1,
        )

        image_url = response.data[0].url
        return image_url
