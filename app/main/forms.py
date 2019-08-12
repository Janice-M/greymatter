from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SubmitField,TextAreaField,RadioField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError



class PitchForm(FlaskForm):
	title = StringField('Title', validators=[Required()])
	body = TextAreaField("Rafiki, what would you like to share?",validators=[Required()])
	
	submit = SubmitField('Submit:)')

class CommentForm(FlaskForm):
	description = TextAreaField('What do you think?',validators=[Required()])
	submit = SubmitField()

class UpvoteForm(FlaskForm):
	submit = SubmitField('Submit:)')


class Downvote(FlaskForm):
	submit = SubmitField('Submit:)')