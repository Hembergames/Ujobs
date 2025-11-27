from flask import Flask, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from models import Message, User, Company
import pytz
from db import db
import os
from forms import LoginForm, RegisterForm, ProfileForm, SearchForm


app = Flask (__name__)
app.secret_key = 'secretkey'
lm = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)


@lm.user_loader
def load_user(user_id):
    # user_id = "user-1" ou "company-3"
    tipo, uid = user_id.split("-")
    uid = int(uid)

    if tipo == "user":
        return User.query.get(uid)
    else:
        return Company.query.get(uid)   


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/explore', methods=['GET', 'POST'])
def explore():
    form = SearchForm()
    filtered_users = []

    if form.validate_on_submit():
        query = form.search.data.strip()
        account_type = form.account_type.data

        if account_type in ["all", "person"]:
            users = User.query.filter(User.name.ilike(f"%{query}%")).all()
            filtered_users.extend(users)

        if account_type in ["all", "company"]:
            companies = Company.query.filter(Company.company_name.ilike(f"%{query}%")).all()
            filtered_users.extend(companies)

    else:
        # exibir todos
        users = User.query.all()
        companies = Company.query.all()
        filtered_users.extend(users)
        filtered_users.extend(companies)

    return render_template('explore.html', users=filtered_users, form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data  # corrigi aqui: use .data, não passwordLogin

        # Tenta achar o usuário
        user = User.query.filter_by(user=username).first()

        # Se não achar, tenta como empresa
        if not user:
            user = Company.query.filter_by(user=username).first()

        # Se ainda assim não existir
        if not user:
            flash("Usuário não encontrado.", "danger")
            return redirect(url_for('login'))

        # Verifica senha
        if user.password != password:
            flash("Senha incorreta.", "danger")
            return redirect(url_for('login'))

        # Faz login
        login_user(user)

        # Redireciona sempre para home
        return redirect(url_for('home'))

    return render_template("login.html", form=form)


from flask_login import logout_user
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Verifica usuário duplicado
        if User.query.filter_by(user=form.username.data).first() or Company.query.filter_by(user=form.username.data).first():
            flash("Esse nome de usuário já está em uso!", "danger")
            return redirect("/register")

        if form.password.data != form.password_again.data:
            flash("As senhas não coincidem!", "danger")
            return redirect("/register")

        # ========================= Pessoa Física =========================
        if form.accountType.data == "person":
            if form.cpf.data and User.query.filter_by(cpf=form.cpf.data).first():
                flash("Este CPF já está cadastrado!", "danger")
                return redirect("/register")

            new_user = User(
                user=form.username.data,
                password=form.password.data,
                cpf=form.cpf.data,
                name=form.name.data,
                date=form.birth_date.data,
                email=form.email.data,
                number=form.number.data,
                bio=form.bio.data,
                account_type="person"
            )

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash("Conta criada com sucesso!", "success")
            return redirect(url_for('home'))

        # ========================= Empresa =========================
        else:
            if form.cnpj.data and Company.query.filter_by(cnpj=form.cnpj.data).first():
                flash("Este CNPJ já está cadastrado!", "danger")
                return redirect("/register")

            new_company = Company(
                user=form.username.data,
                password=form.password.data,
                cnpj=form.cnpj.data,
                company_name=form.company_name.data,
                email=form.email.data,
                number=form.number.data,
                bio=form.bio.data
            )

            db.session.add(new_company)
            db.session.commit()
            login_user(new_company)
            flash("Empresa cadastrada com sucesso!", "success")
            return redirect(url_for('home'))

    return render_template("register.html", form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    min_date = datetime(1909, 1, 1).date()
    max_date = (datetime.utcnow() - relativedelta(years=18)).date()

    is_empresa = isinstance(current_user, Company)

    if form.validate_on_submit():
        # ---------------- Pessoa Física ----------------
        if not is_empresa:
            current_user.name = form.name.data
            current_user.date = form.birth_date.data
            current_user.cpf = form.cpf.data

            if form.photo.data:
                filename = secure_filename(form.photo.data.filename)
                file_path = os.path.join(current_app.root_path, 'static/uploads', filename)
                form.photo.data.save(file_path)
                current_user.photo = f'uploads/{filename}'

        # ---------------- Empresa ----------------
        else:
            empresa_campos = [
                'company_name', 'cnpj', 'territorial_scope', 'business_sector',
                'website_url', 'job_positions', 'structure_type', 'headquarters_address'
            ]
            for field in empresa_campos:
                setattr(current_user, field, getattr(form, field).data)

            if form.logo.data:
                filename = secure_filename(form.logo.data.filename)
                file_path = os.path.join(current_app.root_path, 'static/uploads', filename)
                form.logo.data.save(file_path)
                current_user.logo = f'uploads/{filename}'

        # ---------------- Campos comuns ----------------
        current_user.email = form.email.data
        current_user.number = form.number.data
        current_user.bio = form.bio.data

        db.session.commit()
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for('profile'))

    # ------------- GET: Preencher o formulário -------------
    if request.method == 'GET':
        if not is_empresa:
            form.name.data = getattr(current_user, 'name', '')
            form.birth_date.data = getattr(current_user, 'date', None)
            form.cpf.data = getattr(current_user, 'cpf', '')
        else:
            for field in ['company_name', 'cnpj', 'territorial_scope', 'business_sector',
                          'website_url', 'job_positions', 'structure_type', 'headquarters_address']:
                getattr(form, field).data = getattr(current_user, field, '')

        # Campos comuns
        form.email.data = getattr(current_user, 'email', '')
        form.number.data = getattr(current_user, 'number', '')
        form.bio.data = getattr(current_user, 'bio', '')

    return render_template('profile.html', form=form, min_date=min_date, max_date=max_date, current_user=current_user)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/<username>')
def profiles(username):
    # Primeiro tenta User
    account = User.query.filter_by(user=username).first()
    
    # Se não achar, tenta Company
    if not account:
        account = Company.query.filter_by(user=username).first_or_404()

    # Se for o próprio usuário/empresa logado
    if account == current_user:
        return profile()

    idade = None
    if hasattr(account, 'date') and account.date:
        hoje = date.today()
        idade = hoje.year - account.date.year - ((hoje.month, hoje.day) < (account.date.month, account.date.day))

    return render_template('profiles.html', user=account, idade=idade)



@app.route("/chat/<int:with_user_id>", methods=["GET", "POST"])
@login_required
def chat(with_user_id):
    other = User.query.get_or_404(with_user_id)

    if request.method == "POST":
        text = request.form.get("message")

        if text.strip():
            msg = Message(
                sender_id=current_user.id,
                receiver_id=with_user_id,
                content=text,
                timestamp=datetime.now(pytz.timezone("America/Sao_Paulo"))
            )
            db.session.add(msg)
            db.session.commit()

        return redirect(url_for("chat", with_user_id=with_user_id))

    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == with_user_id)) |
        ((Message.sender_id == with_user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    return render_template("chat.html", other=other, messages=messages)


@app.route('/chats')
@login_required
def conversations():

    msgs = Message.query.filter(
        (Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)
    ).order_by(Message.timestamp.desc()).all()

    conv_map = {}
    for m in msgs:

        if m.sender_id == current_user.id:
            partner_id = m.receiver_id
        else:
            partner_id = m.sender_id

        if partner_id not in conv_map:
            conv_map[partner_id] = {
                'message': m.content,
                'timestamp': m.timestamp,
                'partner_id': partner_id,
                'partner': m.sender if m.sender_id != current_user.id else m.receiver
            }

    conversations = sorted(conv_map.values(), key=lambda x: x['timestamp'], reverse=True)

    return render_template('chats.html', conversations=conversations)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)