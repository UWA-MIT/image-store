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

    seller = so.relationship('User', foreign_keys=[seller_id], backref='products_selling')

    def generate_image(name):

        # Implement AI image generation logic here
        
        return None