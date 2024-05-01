# Importing necessary modules
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import current_app
from app import db
from app.models.product import Product

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

# Basic reward model to keep track of rewards
class Reward(db.Model):
    # Database columns
    id = sa.Column(sa.Integer, primary_key=True)
    reason = sa.Column(sa.String(100))  # Reason for reward addition/deduction
    reward_type = sa.Column(sa.String(20), default="Credit")  # Type of reward: Debit/Credit
    amount = sa.Column(sa.Integer())  # Reward amount
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), index=True)  # Associated user
    timestamp = sa.Column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))  # Timestamp

    # Relationship with User model
    user = so.relationship('User', foreign_keys=[user_id], backref='reward_user')

    # Representation of Reward object
    def __repr__(self):
        return '<Reward {} {}>'.format(self.id, self.reason)

    # Method to calculate total credit rewards
    def total_credit_rewards():
        total_credit_rewards = Reward.query.filter_by(reward_type='Credit').with_entities(func.sum(Reward.amount)).scalar() or 0
        return total_credit_rewards

    # Generic reusable method to apply or deduct a reward to a user account
    def applyReward(reason:str, amount:int, user_id:int, reward_type:str = "Credit"):
        try:
            reward_type_string = reward_type
            if (reward_type == 'Initialize'):
                reward_type_string = 'Credit'

            # Create a new reward object
            reward = Reward(reason=reason, amount=amount, reward_type=reward_type_string, user_id=user_id)
            db.session.add(reward)
            db.session.commit()

            # Fetch the related user object through the relationship
            user = reward.user
            if user:
                # Update the user's money field based on the reward type
                if (reward_type == 'Initialize'):
                    user.money = amount
                elif (reward_type == 'Debit'):
                    user.money -= amount
                else:
                    user.money += amount

                db.session.add(user)
                db.session.commit()

            return True  # Return True to indicate success
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback changes in case of error
            print(f"Error applying reward: {e}")
            return False  # Return False to indicate failure

    # Method to apply a bonus for user registration
    def addRewardForRegistration(user_id):
        amount = current_app.config['REWARD_MONEY_FOR_REGISTRATION']
        return Reward.applyReward(reason="User registration bonus.", amount=amount, reward_type="Initialize", user_id=user_id)

    # Method to deduct reward for image generation
    def deductRewardForImageGeneration(user_id, product_id):
        amount = current_app.config['REWARD_MONEY_FOR_GENERATE_PRODUCT']
        return Reward.applyReward(reason=f"Generated an image (Ref# {product_id}).", amount=int(amount), reward_type="Debit", user_id=user_id)

    # Method to deduct reward for a purchase event
    def deductRewardForPurchase(user_id, product_id, amount):
        return Reward.applyReward(reason=f"Purchased an image (Ref# {product_id}).", amount=int(amount), reward_type="Debit", user_id=user_id)

    # Method to add reward for purchasing from the same user multiple times
    def addRewardForPurchaseFromSameUserIfApplicable(user_id, product_id, seller_id):
        number_of_purchases = current_app.config['PURCHASE_COUNT_FOR_SAME_USER']
        amount = current_app.config['REWARD_MONEY_FOR_PURCHASE_SAME_USER']

        product_count = Product.query.filter_by(seller_id=seller_id, buyer_id=user_id).count()
        if (int(product_count) != int(number_of_purchases)):
            return True  # Do not execute anything if the condition is not met

        return Reward.applyReward(reason=f"Purchased {int(product_count)} item(s) from same seller (Ref# {seller_id}).", amount=int(amount), reward_type="Credit", user_id=user_id)

    # Method to add reward for purchasing products of the same type multiple times
    def addRewardForPurchaseOfSameType(user_id, product_id, category):
        number_of_purchases = current_app.config['PURCHASE_COUNT_FOR_SAME_TYPE']
        amount = current_app.config['REWARD_MONEY_FOR_PURCHASE_SAME_TYPE']

        product_count = Product.query.filter_by(category=category, buyer_id=user_id).count()
        if (int(product_count) != int(number_of_purchases)):
            return True  # Do not execute anything if the condition is not met

        return Reward.applyReward(reason=f"Purchased {int(product_count)} item(s) from same seller (Ref# {seller_id}).", amount=int(amount), reward_type="Credit", user_id=user_id)
