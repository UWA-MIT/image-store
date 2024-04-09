from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Product(db.Model):
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

    seller = so.relationship('User', foreign_keys=[seller_id], backref='products_selling')

    def generate_image(category):
        from openai import OpenAI
        client = OpenAI()
        client.api_key = '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'
        response = client.images.generate(
            model="dall-e-2",
            prompt=category,
            n=1,
            size="256x256"
        )
        return response.data[0].url