from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, Optional, DataRequired

class LoginForm(FlaskForm):

    email = StringField(label='Email', validators=[InputRequired(), Email()], render_kw={'placeholder': 'Email Address'})
    password = PasswordField(label='Password', validators=[InputRequired()], render_kw={'placeholder': 'Password'})
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField(label='Login')

class SignupForm(FlaskForm):

    email = StringField(label='Email', validators=[InputRequired(), Email()], render_kw={'placeholder': 'Email Address'})
    username = StringField(label='Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Username'})
    password = PasswordField(label='Password', validators=[InputRequired(), Length(min=6, max=20)], render_kw={'placeholder': 'Password'})
    confirm_password = PasswordField(label='Confirm Password', validators=[InputRequired(), EqualTo('password')], render_kw={'placeholder': 'Confirm Password'})
    phone_number = StringField(label='Phone Number', validators=[Optional()], render_kw={'placeholder': 'Phone Number (Optional)'})
    # impairment = SelectField(label='Impairment', validators=[DataRequired()], choices=[(1, 'None'), (2, 'Deaf'), (3, 'Mute')])
    submit = SubmitField(label='Sign-Up')

