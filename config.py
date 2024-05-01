import os
from dotenv import load_dotenv

# Get the absolute path of the directory containing the current file
basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from the .flaskenv file
load_dotenv(os.path.join(basedir, '.flaskenv'))

class Config:
    """
    Configuration settings for the Flask application.
    """

    # Secret key for session management and password hashing
    SECRET_KEY = os.environ.get('SECRET_KEY') or '52e4da2524c9580fd6bcff60fab06189'

    # Database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # Disable modification tracking
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email server settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin@student.uwa.edu.au']

    # OpenAI API key
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

    # Pagination settings
    POSTS_PER_PAGE = 10

    # Reward settings
    REWARD_MONEY_FOR_GENERATE_PRODUCT = 3
    REWARD_MONEY_FOR_REGISTRATION = 100
    PURCHASE_COUNT_FOR_SAME_USER = 3
    REWARD_MONEY_FOR_PURCHASE_SAME_USER = 15
    PURCHASE_COUNT_FOR_SAME_TYPE = 5
    REWARD_MONEY_FOR_PURCHASE_SAME_TYPE = 25

    # Remember me setting
    REMEMBER_ME_DAYS = 7

class TestConfig(Config):
    """
    Configuration settings for testing environment.
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tests/test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
