from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 

class PokeForm(FlaskForm):
    poke_search = StringField('Name or ID of pokemon', validators=[DataRequired()])
    submit_btn = SubmitField('Find My Pokemon')