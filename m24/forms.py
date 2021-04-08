from flask_wtf import FlaskForm ,Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField , TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo , ValidationError
from m24.models import User
from io import BytesIO
from flask_wtf.file import FileField
class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class ContactForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = StringField('Message',validators=[DataRequired()])
    submit = SubmitField('Send Message')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# class GalleryForm(FlaskForm):
#     picture = FileField("select an image" , validators=[FileAllowed(['jpg' , 'png'])] )


class PostForm(Form):
    title= StringField('Title',validators=[DataRequired()])
    content = TextAreaField('content' , validators=[DataRequired()])
    file = FileField()
    submit = SubmitField('Post')

class AnonymousForm(FlaskForm):
    title= StringField('Title',validators=[DataRequired()])
    content = TextAreaField('content' , validators=[DataRequired()])
    submit = SubmitField('Post')


class UploadForm(Form):
    file = FileField()
    submit = SubmitField("submit")
    download = SubmitField("download")


class uploadVideoForm(Form):
    link = StringField('link',validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField("submit")
