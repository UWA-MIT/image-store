"""
This module defines a FlaskForm for editing user profiles.

The EditProfileForm class defines a form with fields for editing a user's username and about me section.
It also includes validation logic to ensure unique usernames.

Classes:
    EditProfileForm: A FlaskForm for editing user profiles.

Attributes:
    username: StringField - Field for entering the new username.
    about_me: TextAreaField - Field for entering information about the user.
    submit: SubmitField - Button for submitting the form.

Methods:
    __init__: Initializes the EditProfileForm instance.
    validate_username: Validates the uniqueness of the entered username.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length

import sqlalchemy as sa
from app import db
from app.models.user import User

class EditProfileForm(FlaskForm):
    """
    A form for editing user profiles.
    """

    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        """
        Initialize the EditProfileForm instance.

        Args:
            original_username (str): The original username of the current user.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        """
        Validate the uniqueness of the entered username.

        Args:
            username (str): The username to validate.

        Raises:
            ValidationError: If the entered username is not unique.
        """
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(User.username == self.username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')
