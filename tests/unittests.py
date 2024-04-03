# cd tests -> python -m unittest unittests.py
import unittest, sys
sys.path.append('../')
from config import TestConfig
from app import create_app, db
from app.models.user import User

app = create_app(TestConfig)

class Test(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        user1 = User(username='Konstantin', email='24090236@student.uwa.edu.au')
        user2 = User(username='Ivan', email='test@mail.ru')
        db.session.add(user1)
        db.session.add(user2)
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



if __name__ == '__main__':
    unittest.main()
