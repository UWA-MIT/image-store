from flask import current_app, render_template
from threading import Thread
from flask_mail import Message
from app import mail

def send_async_email(app, msg):
    """
    Send email asynchronously.
    
    Args:
        app (Flask): The Flask application context.
        msg (Message): The email message to be sent.
    """
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    """
    Send email with the specified subject, sender, recipients, text body, and HTML body.
    
    Args:
        subject (str): The subject of the email.
        sender (str): The email address of the sender.
        recipients (list): The list of recipient email addresses.
        text_body (str): The text body of the email.
        html_body (str): The HTML body of the email.
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()

def send_password_reset_email(user):
    """
    Send a password reset email to the user.
    
    Args:
        user (User): The user object.
    """
    token = user.get_reset_password_token()
    send_email('[BuySell] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
