from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class PublishPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(1, 100)])
    body = StringField("Body", validators=[DataRequired(), Length(1, 500)])
    submit = SubmitField("Register")


class UpdatePostForm(PublishPostForm):
    submit = SubmitField("Update")
