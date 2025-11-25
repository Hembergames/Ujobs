from flask import Flask, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from datetime import datetime, date
from models import Message, User
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
def user_loader(id):
    user = db.session.query(User).filter_by(id=id).first()
    return user


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/explore', methods=['GET', 'POST'])
def explore():
    form = SearchForm()
    users = []

    if form.validate_on_submit():
        query = form.search.data.strip()
        users = User.query.filter(User.name.ilike(f"%{query}%")).all()
    else:
        users = User.query.all()

    return render_template('explore.html', users=users, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logout_user()

    form = LoginForm()
    if form.validate_on_submit():
        user = form.userLogin.data
        password = form.passwordLogin.data
        user = db.session.query(User).filter_by(user=user, password=password).first()

        if user:
            login_user(user)
            return redirect(url_for('home'))
        
        else:
            flash('Usuário ou senha inválidos!', 'danger')
  
    return render_template('login.html', form=form)
    

from flask_login import logout_user

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        logout_user()
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = form.userLogin.data
        password = form.passwordLogin.data
        passwordAgain = form.passwordAgainLogin.data

        if db.session.query(User).filter_by(user=user).first():
            flash('Esse usuário já existe!', 'danger')
        elif password != passwordAgain:
            flash('As senhas são diferentes!', 'danger')
        else:
            new_user = User(user=user, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
    
    return render_template('register.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.nameProfile.data
        current_user.date = form.dateProfile.data
        current_user.email = form.emailProfile.data
        current_user.number = form.numberProfile.data
        current_user.bio = form.bioProfile.data

        if form.photoProfile.data:
            filename = secure_filename(form.photoProfile.data.filename)
            file_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            form.photoProfile.data.save(file_path)
            current_user.photo = f'uploads/{filename}'
        
        db.session.commit()
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for('profile'))
    
    elif request.method == 'POST':
        flash("Alguma informação inválida!", "danger")
        return redirect(url_for('profile'))
        
    
    form.nameProfile.data = current_user.name
    form.dateProfile.data = current_user.date
    form.emailProfile.data = current_user.email
    form.numberProfile.data = current_user.number
    form.bioProfile.data = current_user.bio

    return render_template('profile.html', form=form)
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/<username>')
def profiles(username):
    user = User.query.filter_by(user=username).first_or_404()

    if user == current_user:
        return profile()

    idade = None
    if user.date:
        hoje = date.today()
        idade = hoje.year - user.date.year - ((hoje.month, hoje.day) < (user.date.month, user.date.day))

    return render_template('profiles.html', user=user, idade=idade)


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