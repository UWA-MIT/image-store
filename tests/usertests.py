# Run the app with FLASK_CONFIG = 'test' before running the test.
# cd tests -> python -m unittest usertests.py, python -m unittest usertests.Test.testEditProfile
import unittest, sys
sys.path.append('../')
from config import TestConfig
from app import create_app, db
from app.models.user import User
from app.models.product import Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import os

app = create_app(TestConfig)
basedir = os.path.abspath(os.path.dirname(__file__))


class Test(unittest.TestCase):
    def setUp(self):
        service = Service(executable_path=r'chromedriver.exe')
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')  # Run Chrome in headless mode.
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.driver.set_window_size(1920, 1080)
        self.driver.get('http://127.0.0.1:5000')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.driver.quit()

    def testLoginAndLogout(self):
        user = self.createUser()
        self.login(user)
        logout = self.driver.find_element(By.ID, "logout")
        logout.click()
        username = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        password = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        assert username.is_displayed(), "The username element is not visible."
        assert password.is_displayed(), "The password element is not visible."


    def testRegistration(self):
        self.driver.get('http://127.0.0.1:5000/auth/register')
        username = self.driver.find_element(By.ID, "username")
        name = self.driver.find_element(By.ID, "name")
        email = self.driver.find_element(By.ID, "email")
        password = self.driver.find_element(By.ID, "password")
        password2 = self.driver.find_element(By.ID, "password2")
        submit = self.driver.find_element(By.ID, "submit")
        username.send_keys('Konstantin2')
        name.send_keys('KonstantinTagintsev')
        email.send_keys('240902362@student.uwa.edu.au')
        password.send_keys('test123')
        password2.send_keys('test123')
        submit.click()
        user = self.getUserById(1)
        self.assertTrue(user.username == 'Konstantin2')
        self.assertTrue(user.name == 'KonstantinTagintsev')
        self.assertTrue(user.email == '240902362@student.uwa.edu.au')
        self.assertTrue(user.check_password('test123'))

    def testResetPassword(self):
        user = self.createUser()
        self.driver.get('http://127.0.0.1:5000/auth/login')
        reset = self.driver.find_element(By.ID, "resetPassword")
        reset.click()
        email = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        email.send_keys(user.email)
        submit = self.driver.find_element(By.ID, "submit")
        submit.click()
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-info"))
        )
        expected_text = "Check your email for the instructions to reset your password"
        actual_text = element.text
        assert expected_text == actual_text, f"Expected text '{expected_text}' did not match actual text '{actual_text}'."

    def testChangePassword(self):
        user = self.createUser()
        self.login(user)
        self.driver.get('http://127.0.0.1:5000/auth/change_password')
        current_password = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "current_password"))
        )
        password = self.driver.find_element(By.ID, "password")
        password2 = self.driver.find_element(By.ID, "password2")
        current_password.send_keys('test123')
        password.send_keys('test111')
        password2.send_keys('test111')
        submit = self.driver.find_element(By.ID, "submit")
        submit.click()
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-info"))
        )
        expected_text = "Your password has been changed."
        actual_text = element.text
        assert expected_text == actual_text, f"Expected text '{expected_text}' did not match actual text '{actual_text}'."

    def testViewProfile(self):
        user = self.createUser()
        self.login(user)
        self.driver.get('http://127.0.0.1:5000/users/user/' + user.username)
        username = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#profile .username"))
        )
        expected_text = user.username
        actual_text = username.text
        assert expected_text == actual_text, f"Expected username '{expected_text}' did not match actual username '{actual_text}'."

    def testEditProfile(self):
        user = self.createUser()
        self.login(user)
        self.driver.get('http://127.0.0.1:5000/users/edit_profile')
        aboutMe = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "about_me"))
        )
        submit = self.driver.find_element(By.ID, "submit")
        aboutMe.send_keys('testAboutMe')
        submit.click()
        aboutMe = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#profile .about-me"))
        )
        user = self.refreshUser(user)
        expected_text = 'Bio: ' + user.about_me
        actual_text = aboutMe.text
        assert expected_text == actual_text, f"Expected about_me '{expected_text}' did not match actual about_me '{actual_text}'."

    def testGenerateImage(self):
        user = self.createUser()
        self.login(user)
        self.driver.get('http://127.0.0.1:5000/products/generate_product')
        name = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "name"))
        )
        dropdown = Select(self.driver.find_element(By.ID, "category"))
        price = self.driver.find_element(By.ID, "price")
        submit = self.driver.find_element(By.ID, "submit")
        name.send_keys('Lambo')
        dropdown.select_by_value("car")
        price.send_keys('100')
        submit.click()

        product = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-listing .card.area"))
        )
        element = product.find_element(By.CSS_SELECTOR, ".card-title")
        expected_text = 'LAMBO (CAR)'
        actual_text = element.text
        assert expected_text == actual_text, f"Expected name and category '{expected_text}' did not match actual name and category '{actual_text}'."

        element = product.find_element(By.CSS_SELECTOR, ".card-text .price")
        expected_text = '$100.0'
        actual_text = element.text
        assert expected_text == actual_text, f"Expected price '{expected_text}' did not match actual price '{actual_text}'."

        element = product.find_element(By.CSS_SELECTOR, ".card-img-top")
        path = os.path.join(basedir, '../app/static/images/nft/' + element.get_attribute("src").split('/')[-1])
        print(path)
        os.remove(path)

    def testBuyImage(self):
        user = self.createUser()
        user2 = self.createUser('Ivan', 'ivan@mail.ru', 'student')
        product1, product2 = self.createProducts(2)
        self.login(user)
        self.driver.get('http://127.0.0.1:5000/products/buy')

        product = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-listing .card.area[data-id='" + str(product1.id) + "']"))
        )
        element = product.find_element(By.CSS_SELECTOR, ".card-title")
        expected_text = product1.name.upper() + ' (' + product1.category.upper() + ')'
        actual_text = element.text
        assert expected_text == actual_text, f"Expected name and category '{expected_text}' did not match actual name and category '{actual_text}'."

        element = product.find_element(By.CSS_SELECTOR, ".card-text .price")
        expected_text = '$' + str(product1.price)
        actual_text = element.text
        assert expected_text == actual_text, f"Expected price '{expected_text}' did not match actual price '{actual_text}'."

        buy = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.pretty-btn[data-id='" +  str(product2.id) + "']"))
        )
        buy.click()

        confirm = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@onclick=\"buyImage('" + str(product2.id) + "')\"]"))
        )
        confirm.click()

        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-info"))
        )
        expected_text = "Congratulations, your product purchase has been completed successfully!"
        actual_text = element.text
        assert expected_text == actual_text, f"Expected text '{expected_text}' did not match actual text '{actual_text}'."

    def testMyPurchasesPage(self):
        user = self.createUser()
        product1, product2 = self.createProducts(1, 1, True)
        self.login(user)
        self.driver.get('http://127.0.0.1:5000/products/my_purchases')

        product = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-listing .card.area[data-id='" + str(product1.id) + "']"))
        )
        element = product.find_element(By.CSS_SELECTOR, ".card-title")
        expected_text = product1.name.upper() + ' (' + product1.category.upper() + ')'
        actual_text = element.text
        assert expected_text == actual_text, f"Expected name and category '{expected_text}' did not match actual name and category '{actual_text}'."

        element = product.find_element(By.CSS_SELECTOR, ".card-text .price")
        expected_text = '$' + str(product1.price)
        actual_text = element.text
        assert expected_text == actual_text, f"Expected price '{expected_text}' did not match actual price '{actual_text}'."

    def testSellPage(self):
        user = self.createUser()
        product1, product2 = self.createProducts(1)
        self.login(user)
        self.driver.get('http://127.0.0.1:5000/products/sell')

        product = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-listing .card.area[data-id='" + str(product1.id) + "']"))
        )
        element = product.find_element(By.CSS_SELECTOR, ".card-title")
        expected_text = product1.name.upper() + ' (' + product1.category.upper() + ')'
        actual_text = element.text
        assert expected_text == actual_text, f"Expected name and category '{expected_text}' did not match actual name and category '{actual_text}'."

        element = product.find_element(By.CSS_SELECTOR, ".card-text .price")
        expected_text = '$' + str(product1.price)
        actual_text = element.text
        assert expected_text == actual_text, f"Expected price '{expected_text}' did not match actual price '{actual_text}'."


    def createUser(self, usernam='Konstantin', email='24090236@student.uwa.edu.au', about_me='I am a student'):
        user = User(username = usernam, email = email, about_me=about_me)
        user.set_password('test123')
        db.session.add(user)
        db.session.commit()
        return self.getUserById(1)

    def getUserById(self, id):
        return db.session.get(User, id)

    def refreshUser(self, user):
        db.session.refresh(user)
        return db.session.get(User, user.id)

    def login(self, user):
        self.driver.get('http://127.0.0.1:5000/auth/login')
        username = self.driver.find_element(By.ID, "username")
        password = self.driver.find_element(By.ID, "password")
        submit = self.driver.find_element(By.ID, "submit")
        username.send_keys(user.username)
        password.send_keys('test123')
        submit.click()
        element_xpath = f"//*[contains(text(), 'Hello, {user.username}!')]"
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
        )

    def createProducts(self, seller_id=1, buyer_id=None, is_sold=False):
        product1 = Product(name='Lambo', category='Car', price=100.0, is_sold=is_sold, seller_id=seller_id, buyer_id=buyer_id)
        product2 = Product(name='Small', category='Ant', price=100.0, is_sold=is_sold, seller_id=seller_id, buyer_id=buyer_id)
        db.session.add(product1)
        db.session.add(product2)
        db.session.commit()
        return db.session.get(Product, 1), db.session.get(Product, 2)

    def refreshProducts(self):
        product1 = db.session.get(Product, 1)
        product2 = db.session.get(Product, 2)
        db.session.refresh(product1)
        db.session.refresh(product2)
        return product1, product2