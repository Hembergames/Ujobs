from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    userLogin = StringField(validators=[DataRequired()])
    passwordLogin = PasswordField(validators=[DataRequired()])
    passwordAgainLogin = PasswordField(validators=[DataRequired()])
    login = SubmitField('Entrar')
    register = SubmitField('Criar')