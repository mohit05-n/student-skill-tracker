from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, SelectMultipleField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from models import Skill, Course

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class StudentForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    skills = SelectMultipleField('Skills', coerce=int)
    submit = SubmitField('Add Student')
    
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.skills.choices = [(skill.id, f"{skill.name} ({skill.course})") for skill in Skill.query.all()]

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    skills = SelectMultipleField('Skills', coerce=int)
    submit = SubmitField('Update Profile')
    
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.skills.choices = [(skill.id, f"{skill.name} ({skill.course})") for skill in Skill.query.all()]

class CertificationForm(FlaskForm):
    name = StringField('Certification Name', validators=[DataRequired()])
    issuer = StringField('Issuer', validators=[DataRequired()])
    issue_date = DateField('Issue Date', validators=[DataRequired()])
    expiry_date = DateField('Expiry Date', validators=[Optional()])
    credential_id = StringField('Credential ID', validators=[Optional()])
    submit = SubmitField('Add Certification')
