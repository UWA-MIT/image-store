from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length

class GenerateProductForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Prompt text', validators=[Length(min=3, max=256)])
    price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')
