from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

from wtforms import TextAreaField

import sqlalchemy as sa
from app import db
from app.models.product import Product


class GenerateProductForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Prompt text', validators=[Length(min=0, max=256)])
    price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')
