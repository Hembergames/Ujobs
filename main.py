from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db import db
from models import User
from forms import LoginForm


app = Flask (__name__)
app.secret_key = 'secretkey'
lm = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)


@lm.user_loader
def user_loader(id):
    user = db.session.query(User).filter_by(id=id).first()
    return user


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.userLogin.data
        password = form.passwordLogin.data
        user = db.session.query(User).filter_by(user=user,password=password).first()

        if user:
            login_user(user)
            return redirect(url_for('home'))
        
        else:
            return 'Usuário/Senha inválidos'
  
    return render_template('login.html', form=form)
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.userLogin.data
        password = form.passwordLogin.data
        passwordAgain = form.passwordAgainLogin.data

        if db.session.query(User).filter_by(user=user).first():
            return 'Esse usuário já existe!'
        
        elif password!=passwordAgain:
            return 'As senhas são diferentes!'

        else:
            new_user = User(user=user, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
    
    return render_template('register.html', form=form)
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/profile')
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)