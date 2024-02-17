from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 

class PokeForm(FlaskForm):
    poke_search = StringField('Name or ID of pokemon', validators=[DataRequired()])
    submit = SubmitField('Find My Pokemon')

    # look at dylans github and look at the config also html forms (login page)
    # Also look at login rout to see how that data routes