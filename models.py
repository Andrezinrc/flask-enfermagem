from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy()
db.init_app(app)

class Enfermagem(db.Model):
    __tablename__ = 'notas'
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False)
    descricao_paciente = db.Column(db.String(200), nullable=False)
    terminologia = db.Column(db.String(50), nullable=False)
    sinais_vitais = db.Column(db.String(100), nullable=False)
    nome_paciente = db.Column(db.String(100), nullable=False)
    nome_enfermeiro = db.Column(db.String(100), nullable=False)