from db import db
from flask_login import UserMixin
from datetime import datetime
import pytz

# ========================= Pessoa Física =========================
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=True)
    name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), nullable=True)
    number = db.Column(db.String(20), nullable=True)
    date = db.Column(db.Date, nullable=True)
    bio = db.Column(db.String(1000), nullable=True)
    photo = db.Column(db.String(120), nullable=True)
    account_type = db.Column(db.String(20), nullable=False)   # "person"

    def get_id(self):
        return f"user-{self.id}"


# ========================= Empresa =========================
class Company(UserMixin, db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    cnpj = db.Column(db.String(20), unique=True, nullable=True)
    company_name = db.Column(db.String(80), nullable=True)
    logo = db.Column(db.String(120), nullable=True)
    territorial_scope = db.Column(db.String(50), nullable=True)
    business_sector = db.Column(db.String(50), nullable=True)
    website_url = db.Column(db.String(100), nullable=True)
    job_positions = db.Column(db.String(100), nullable=True)
    structure_type = db.Column(db.String(50), nullable=True)
    headquarters_address = db.Column(db.String(100), nullable=True)
    
    # Campos comuns
    email = db.Column(db.String(80), nullable=True)
    number = db.Column(db.String(20), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    def get_id(self):
        return f"company-{self.id}"



# ==========================================================
#                      MESSAGES
# ==========================================================
class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)

    # Quem enviou
    sender_type = db.Column(db.String(10), nullable=False)   # user / company
    sender_id = db.Column(db.Integer, nullable=False)

    # Quem recebeu
    receiver_type = db.Column(db.String(10), nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)

    content = db.Column(db.String(500), nullable=False)

    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone("America/Sao_Paulo"))
    )
