from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired

class GenerateProductForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[('car', 'Car'), ('nature', 'Nature'), ('tree', 'Tree'), ('food', 'Food'), ('ant', 'Ant')], validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')
