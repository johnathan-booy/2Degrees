from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])


class SignUpForm(LoginForm):
    """Form for adding users."""
    email = EmailField('E-mail', validators=[DataRequired()])
    first_name = StringField('First Name (optional)')
    last_name = StringField('Last Name (optional)')
