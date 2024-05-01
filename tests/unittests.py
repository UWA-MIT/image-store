# cd tests -> python -m unittest unittests.py
import unittest, sys
sys.path.append('../')
from config import TestConfig
from app import create_app, db
from app.models.user import User
from app.models.product import Product
from app.models.reward import Reward
import os

app = create_app(TestConfig)
basedir = os.path.abspath(os.path.dirname(__file__))

class Test(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        user1 = User(username='Konstantin', email='24090236@student.uwa.edu.au')
        user2 = User(username='Ivan', email='test@mail.ru')
        product1 = Product(name='Lanbo', category='Car', price=100)
        product2 = Product(name='Small', category='Ant', price=100)
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(product1)
        db.session.add(product2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def testPasswordHashing(self):
        user1 = db.session.get(User, 1)
        user2 = db.session.get(User, 2)
        user1.set_password('test123')
        user2.set_password('test456')
        self.assertTrue(user1.username == 'Konstantin')
        self.assertTrue(user2.username == 'Ivan')
        self.assertFalse(user1.check_password('lal'))
        self.assertFalse(user2.check_password('lol'))
        self.assertTrue(user1.check_password('test123'))
        self.assertTrue(user2.check_password('test456'))

    def testResetPasswordToken(self):
        user1 = db.session.get(User, 1)
        user2 = db.session.get(User, 2)
        user1.set_password('test123')
        user2.set_password('test456')
        self.assertTrue(user1.username == user1.verify_reset_password_token(user1.get_reset_password_token()).username)
        self.assertTrue(user2.username == user2.verify_reset_password_token(user2.get_reset_password_token()).username)
        self.assertFalse(user1.username == user1.verify_reset_password_token(user2.get_reset_password_token()).username)
        self.assertFalse(user2.username == user2.verify_reset_password_token(user1.get_reset_password_token()).username)

    def testGenerateImage(self):
        product1 = db.session.get(Product, 1)
        filename = product1.generate_image(product1.name, product1.category)
        path = os.path.join(basedir, '../app/static/images/nft/' + filename)
        self.assertTrue(os.path.exists(path))
        self.assertFalse(os.path.exists(path + 'lal'))
        os.remove(path)

    def testApplyReward(self):
        result = Reward.applyReward(reason="Test reward", amount=100, user_id=1)
        self.assertTrue(result)
        reward = Reward.query.filter_by(user_id=1).first()
        self.assertIsNotNone(reward)
        self.assertEqual(reward.amount, 100)

    def testAddRewardForRegistration(self):
        result = Reward.addRewardForRegistration(user_id=1)
        self.assertTrue(result)
        reward = Reward.query.filter_by(user_id=1, reason="User registration bonus.").first()
        self.assertIsNotNone(reward)

    def testDeductRewardForImageGeneration(self):
        product = Product(name='TestProduct', category='TestCategory', price=100)
        db.session.add(product)
        db.session.commit()
        result = Reward.deductRewardForImageGeneration(user_id=1, product_id=product.id)
        self.assertTrue(result)
        reward = Reward.query.filter_by(user_id=1, reason=f"Generated an image (Ref# {product.id}).").first()
        self.assertIsNotNone(reward)

    def testDeductRewardForPurchase(self):
        product = Product(name='TestProduct', category='TestCategory', price=100)
        db.session.add(product)
        db.session.commit()
        result = Reward.deductRewardForPurchase(user_id=1, product_id=product.id, amount=100)
        self.assertTrue(result)
        reward = Reward.query.filter_by(user_id=1, reason=f"Purchased an image (Ref# {product.id}).").first()
        self.assertIsNotNone(reward)

    def testAddRewardForPurchaseFromSameUserIfApplicable(self):
        seller = User(username='TestSeller', email='testseller@mail.com')
        db.session.add(seller)
        db.session.commit()
        product = Product(name='TestProduct', category='TestCategory', price=100, seller_id=seller.id, buyer_id=1)
        db.session.add(product)
        db.session.commit()
        result = Reward.addRewardForPurchaseFromSameUserIfApplicable(user_id=1, product_id=product.id, seller_id=seller.id)
        self.assertTrue(result)

    def testAddRewardForPurchaseOfSameType(self):
        product = Product(name='TestProduct', category='TestCategory', price=100, buyer_id=1)
        db.session.add(product)
        db.session.commit()
        result = Reward.addRewardForPurchaseOfSameType(user_id=1, product_id=product.id, category=product.category)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
