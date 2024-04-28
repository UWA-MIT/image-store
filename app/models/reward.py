from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import current_app
from app import db

from sqlalchemy.exc import SQLAlchemyError

# This is a basic reward model which will keep record of all the rewards
class Reward( db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    reason = sa.Column(sa.String(100)) # What this reward is added / deducted for.
    reward_type = sa.Column(sa.String(20), default="Credit") # Debit / Credit
    amount = sa.Column(sa.Integer()) 
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), index=True)
    timestamp = sa.Column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))

    user = so.relationship('User', foreign_keys=[user_id], backref='reward_user')

    def __repr__(self):
        return '<Reward {} {}>'.format(self.id, self.reason)

    
    def addRewardForRegistration(user_id):
        # This function apply a bonus for user registration.
        # this function should be used in static context
        # this function will override default money value of the field with value from configrations.
        # @static
        try:
            amount = current_app.config['REWARD_MONEY_FOR_REGISTRATION']
            reward = Reward(reason="User registration bonus.", amount=amount, reward_type="Credit", user_id=user_id)
            db.session.add(reward)
            db.session.commit()

            # Fetch the related user object through the relationship
            user = reward.user
            if user:
                # Update the user's money field
                user.money = int(amount)
                db.session.add(user)
                db.session.commit()

            return True  # Return True to indicate success
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback changes in case of error
            print(f"Error applying reward: {e}")
            return False  # Return False to indicate failure

    def deductRewardForImageGeneration(user_id, product_id):
        # This function add a deduction record in the database for an image generation event.
        # This will not udpate User.money as it has already been deducted during purchase.
        # @static
        try:
            amount = current_app.config['REWARD_MONEY_FOR_GENERATE_PRODUCT']
            reward = Reward(reason=f"Generated an image (Ref# {product_id}).", amount=int(amount), reward_type="Debit", user_id=user_id)
            db.session.add(reward)
            db.session.commit()

            # Fetch the related user object through the relationship
            user = reward.user
            if user:
                # Update the user's money field
                user.money -= int(amount)
                db.session.add(user)
                db.session.commit()

            return True 
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback changes in case of error
            print(f"Error applying reward: {e}")
            return False 


    def deductRewardForPurchase(user_id, product_id, amount):
        # This function add a deduction record in the database for an purchase event.
        # This will not udpate User.money as it has already been deducted during purchase.
        # @static
        try:
            reward = Reward(reason=f"Purchased an image (Ref# {product_id}).", amount=int(amount), reward_type="Debit", user_id=user_id)
            db.session.add(reward)
            db.session.commit()

            # Fetch the related user object through the relationship
            user = reward.user
            if user:
                # Update the user's money field
                user.money -= int(amount)
                db.session.add(user)
                db.session.commit()

            return True 
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback changes in case of error
            print(f"Error applying reward: {e}")
            return False 


    


