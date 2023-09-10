# Übernommen aus den Beispielen
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User

# Übernommen aus den Beispielen
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Übernommen aus den Beispielen
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Übernommen aus den Beispielen
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

# Übernommen aus den Beispielen
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

# Eigenentwicklung
class New3DPrint(FlaskForm):
    name = StringField('Filename', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Printed','Printed'),('Not printed','Not printed')], validators=[DataRequired()])
    quality = SelectField('Printquality', choices=[('Fabulous','Fabulous'),('Good','Good'),('Meh','Meh'),('Bad','Bad')], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Eigenentwicklung
class Edit3DPrint(FlaskForm):
    status = SelectField('Status', choices=[('Printed','Printed'),('Not printed','Not printed')], validators=[DataRequired()])
    quality = SelectField('Printquality', choices=[('Fabulous','Fabulous'),('Good','Good'),('Meh','Meh'),('Bad','Bad')], validators=[DataRequired()])
    submit = SubmitField('Update')