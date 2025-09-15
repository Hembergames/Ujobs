from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, Length, Regexp, Optional
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    userLogin = StringField(validators=[DataRequired()])
    passwordLogin = PasswordField(validators=[DataRequired()])
    login = SubmitField('Entrar na conta')

class RegisterForm(FlaskForm):
    userLogin = StringField(validators=[DataRequired(), Length(max=40)])
    passwordLogin = PasswordField(validators=[DataRequired(), Length(min=8, max=30)])
    passwordAgainLogin = PasswordField(validators=[DataRequired(), Length(min=8, max=30)])
    register = SubmitField('Criar conta')

class ProfileForm(FlaskForm):
    nameProfile = StringField(validators=[Optional(), Length(max=40)])
    dateProfile = DateField(format='%Y-%m-%d', validators=[Optional()])
    emailProfile = StringField(validators=[Optional(), Email(), Length(max=50)])
    numberProfile = StringField(validators=[Optional(), Length(max=15)])
    bioProfile = TextAreaField(validators=[Optional(), Length(max=1000)])
    photoProfile = FileField('Foto de perfil', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens!')])
    save = SubmitField('Salvar')

class SearchForm(FlaskForm):
    search = StringField("Buscar usuário")
    submit = SubmitField("Pesquisar")
    