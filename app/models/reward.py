from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import current_app
from app import db
from app.models.product import Product

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

    def applyReward(reason:str, amount:int, user_id:int, reward_type:str = "Credit"):
        # This is a generic method to apply reward to a user account. 
        # Using this method provides a re-usable way to implement various reward types and senerios
        # @static
        try:
            reward_type_string = reward_type
            if (reward_type == 'Initialize'):
                reward_type_string = 'Credit'

            reward = Reward(reason=reason, amount=amount, reward_type=reward_type_string, user_id=user_id)
            db.session.add(reward)
            db.session.commit()

            # Fetch the related user object through the relationship
            user = reward.user
            if user:

                # Update the user's money field
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

    
    def addRewardForRegistration(user_id):
        # This function apply a bonus for user registration.
        # this function should be used in static context
        # this function will override default money value of the field with value from configrations.
        # @static
        amount = current_app.config['REWARD_MONEY_FOR_REGISTRATION']
        return Reward.applyReward(reason="User registration bonus.", amount=amount, reward_type="Initialize", user_id=user_id)
        

    def deductRewardForImageGeneration(user_id, product_id):
        # This function add a deduction record in the database for an image generation event.
        # This will not udpate User.money as it has already been deducted during purchase.
        # @static

        amount = current_app.config['REWARD_MONEY_FOR_GENERATE_PRODUCT']
        return Reward.applyReward(reason=f"Generated an image (Ref# {product_id}).", amount=int(amount), reward_type="Debit", user_id=user_id)


    def deductRewardForPurchase(user_id, product_id, amount):
        # This function add a deduction record in the database for an purchase event.
        # This will not udpate User.money as it has already been deducted during purchase.
        # @static
        return Reward.applyReward(reason=f"Purchased an image (Ref# {product_id}).", amount=int(amount), reward_type="Debit", user_id=user_id)

    def addRewardForPurchaseFromSameUserIfApplicable(user_id, product_id, seller_id):
        # Purchase x number of products from the same seller id
        number_of_purchases = current_app.config['PURCHASE_COUNT_FOR_SAME_USER']
        amount = current_app.config['REWARD_MONEY_FOR_PURCHASE_SAME_USER']

        product_count = Product.query.filter_by(seller_id=seller_id, buyer_id=user_id).count()
        if (int(product_count) != int(number_of_purchases)):
            return True # do not execute anything

        return Reward.applyReward(reason=f"Purchased {int(product_count)} item(s) from same seller (Ref# {seller_id}).", amount=int(amount), reward_type="Credit", user_id=user_id)

    def addRewardForPurchaseOfSameType(user_id, product_id, category):

        number_of_purchases = current_app.config['PURCHASE_COUNT_FOR_SAME_TYPE']
        amount = current_app.config['REWARD_MONEY_FOR_PURCHASE_SAME_TYPE']  


        product_count = Product.query.filter_by(category=category, buyer_id=user_id).count()
        if (int(product_count) != int(number_of_purchases)):
            return True # do not execute anything

        return Reward.applyReward(reason=f"Purchased {int(product_count)} item(s) from same seller (Ref# {seller_id}).", amount=int(amount), reward_type="Credit", user_id=user_id)


