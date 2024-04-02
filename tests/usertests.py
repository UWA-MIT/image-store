# Run the app with FLASK_CONFIG = 'test' before running the test.
# cd tests -> python -m unittest usertests.py
import unittest, sys
sys.path.append('../')
from config import TestConfig
from app import create_app, db
from app.models.user import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

app = create_app(TestConfig)

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
        user = User(username = 'Konstantin', email = 'k.tagintsev@gmail.com')
        user.set_password('test123')
        db.session.add(user)
        db.session.commit()
        user = db.session.get(User, 1)
        self.driver.get('http://127.0.0.1:5000/auth/login')
        username = self.driver.find_element(By.ID, "username")
        password = self.driver.find_element(By.ID, "password")
        submit = self.driver.find_element(By.ID, "submit")
        username.send_keys(user.username)
        password.send_keys('test123')
        submit.click()
        element_xpath = f"//*[contains(text(), 'Hello, {user.username}!')]"
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, element_xpath)))
        expected_text = f"Hello, {user.username}!"
        actual_text = element.text
        assert expected_text == actual_text, f"Expected text '{expected_text}' did not match actual text '{actual_text}'."

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
        username.send_keys('Konstantin')
        name.send_keys('KonstantinTagintsev')
        email.send_keys('24090236@student.uwa.edu.au')
        password.send_keys('test123')
        password2.send_keys('test123')
        submit.click()
        user = db.session.get(User, 1)
        self.assertTrue(user.username == 'Konstantin')
        self.assertTrue(user.name == 'KonstantinTagintsev')
        self.assertTrue(user.email == '24090236@student.uwa.edu.au')
        self.assertTrue(user.check_password('test123'))