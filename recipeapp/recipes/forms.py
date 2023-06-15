from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, IntegerField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed
from recipeapp.models import Recipe


# Recipe creation Form #
class RecipeCreationForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5)])
    description = TextAreaField('Description', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    prep_time = IntegerField('Preparation Time (mins)', validators=[DataRequired()])
    cook_time = IntegerField('Cooking Time (mins)', validators=[DataRequired()])
    servings = IntegerField('Serving (plates)', validators=[DataRequired()])
    avatar = FileField('Upload Meal Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    submit = SubmitField('Create')
