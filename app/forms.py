# Übernommen aus den Beispielen
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
    TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import Users, Models

# Übernommen aus den Beispielen
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
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
        user = Users.query.filter_by(Username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

# Eigenentwicklung
class New3DPrintForm(FlaskForm):
    name = StringField('Filename', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Printed','Printed'),('Not printed','Not printed')], validators=[DataRequired()])
    quality = SelectField('Printquality', choices=[('Fabulous','Fabulous'),('Good','Good'),('Meh','Meh'),('Bad','Bad')], validators=[DataRequired()])
    submit = SubmitField('Submit')

    # Übernommen aus den Beispielen
    def validate_name(self, name):
        model = Models.query.filter_by(Name=name.data).first()
        if model is not None:
            raise ValidationError('Please use a different filename.')


# Eigenentwicklung
class Edit3DPrintForm(FlaskForm):
    name = StringField('Filename', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Printed','Printed'),('Not printed','Not printed')], validators=[DataRequired()])
    quality = SelectField('Printquality', choices=[('none','none'),('Fabulous','Fabulous'),('Good','Good'),('Meh','Meh'),('Bad','Bad')], validators=[DataRequired()])
    submit = SubmitField('Update')