from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, PasswordField, FileField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional
from flask_wtf.file import FileAllowed


# -------------------- LOGIN --------------------
class LoginForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


# -------------------- REGISTRO --------------------
class RegisterForm(FlaskForm):
    accountType = SelectField(
        "Tipo de conta",
        choices=[("person", "Pessoa Física"), ("company", "Empresa")],
        validators=[DataRequired()]
    )

    username = StringField("Usuário", validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField("Senha", validators=[DataRequired()])
    password_again = PasswordField("Repita a senha", validators=[DataRequired()])

    # Pessoa Física
    cpf = StringField("CPF", validators=[Optional(), Length(max=14)])
    name = StringField("Nome Completo", validators=[Optional(), Length(max=40)])
    birth_date = DateField("Data de nascimento", format='%Y-%m-%d', validators=[Optional()])

    # Empresa
    cnpj = StringField("CNPJ", validators=[Optional(), Length(max=18)])
    company_name = StringField("Nome da empresa", validators=[Optional(), Length(max=120)])

    # Campos comuns
    email = StringField("E-mail", validators=[Optional(), Email(), Length(max=80)])
    number = StringField("Telefone", validators=[Optional(), Length(max=20)])
    bio = TextAreaField("Biografia", validators=[Optional(), Length(max=1000)])

    submit = SubmitField("Criar conta")




class ProfileForm(FlaskForm):
    # Campos pessoa física
    photo = FileField("Foto", validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens!')])
    name = StringField("Nome Completo", validators=[Optional(), Length(max=80)])
    birth_date = DateField("Data de Nascimento", validators=[Optional()])
    cpf = StringField("CPF", validators=[Optional(), Length(max=14)])

    # Campos empresa
    logo = FileField("Logo", validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens!')])
    company_name = StringField("Nome da Empresa", validators=[Optional(), Length(max=80)])
    cnpj = StringField("CNPJ", validators=[Optional(), Length(max=20)])
    
    # Seleção para abrangência territorial
    territorial_scope = SelectField(
        "Abrangência Territorial",
        choices=[
            ('', 'Selecione...'),
            ('local', 'Local'),
            ('regional', 'Regional'),
            ('nacional', 'Nacional'),
            ('internacional', 'Internacional')
        ],
        validators=[Optional()]
    )
    
    business_sector = StringField("Setor de Atuação", validators=[Optional(), Length(max=50)])
    website_url = StringField("Website", validators=[Optional(), Length(max=100)])
    job_positions = StringField("Cargos Oferecidos", validators=[Optional(), Length(max=100)])
    
    # Seleção para tipo de estrutura
    structure_type = SelectField(
        "Tipo de Estrutura",
        choices=[
            ('', 'Selecione...'),
            ('publica', 'Pública'),
            ('privada', 'Privada'),
            ('mista', 'Mista')
        ],
        validators=[Optional()]
    )
    
    headquarters_address = StringField("Endereço da Sede", validators=[Optional(), Length(max=100)])

    # Campos comuns
    email = StringField("E-mail", validators=[Optional(), Email(), Length(max=80)])
    number = StringField("Telefone", validators=[Optional(), Length(max=20)])
    bio = TextAreaField("Biografia", validators=[Optional(), Length(max=1000)])

    save = SubmitField("Salvar")



# -------------------- BUSCA --------------------
class SearchForm(FlaskForm):
    search = StringField("Buscar", validators=[Optional()])
    account_type = SelectField(
        "Tipo de conta",
        choices=[("all", "Todos"), ("person", "Pessoa Física"), ("company", "Empresa")],
        default="all"
    )
    submit = SubmitField("Pesquisar")