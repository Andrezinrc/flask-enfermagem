from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from senha import senha
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{senha}@localhost/enfermagem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

with open('C:/Users/Positivo/Enfermagem_app/data/terminologias.json') as f:
    terminologias = json.load(f)

@app.route('/')
def index():
    notas = Enfermagem.query.all()
    for nota in notas:
        print(f"id: {nota.id}, nome: {nota.nome_paciente}")
    return render_template('index.html')

@app.route("/ver_tabela", methods=["GET"])
def ver_tabela():
    notas = Enfermagem.query.all()
    return render_template("tabela.html", notas=notas)

@app.route('/adicionar', methods=['POST'])
def adicionar_nota():
    data_hora = datetime.strptime(request.form['data_hora'], '%Y-%m-%dT%H:%M')
    descricao_paciente = request.form['descricao_paciente']
    terminologia = request.form['terminologia']
    sinais_vitais = request.form['sinais_vitais']
    nome_paciente = request.form['nome_paciente']
    nome_enfermeiro = request.form['nome_enfermeiro']
    
    nova_nota = Enfermagem(
        data_hora=data_hora,
        descricao_paciente=descricao_paciente,
        terminologia=terminologia,
        sinais_vitais=sinais_vitais,
        nome_paciente=nome_paciente,
        nome_enfermeiro=nome_enfermeiro
    )
    db.session.add(nova_nota)
    db.session.commit()
    return redirect(url_for('ver_tabela'))

@app.route('/sugerir_terminologia')
def sugerir_terminologia():
    termo_digitado = request.args.get('q', '')
    sugeridos = [termo for termo in terminologias if termo_digitado.lower() in termo.lower()]
    return jsonify(sugeridos)

@app.route("/editar_nota/<int:id>", methods=["GET", "POST"])
def editar_nota(id):
    nota = Enfermagem.query.get(id)
    if request.method == "POST":
        nota.data_hora = datetime.strptime(request.form['data_hora'], '%Y-%m-%dT%H:%M')
        nota.descricao_paciente = request.form['descricao_paciente']
        nota.terminologia = request.form['terminologia']
        nota.sinais_vitais = request.form['sinais_vitais']
        nota.nome_paciente = request.form['nome_paciente']
        nota.nome_enfermeiro = request.form['nome_enfermeiro']

        db.session.commit()

        return redirect(url_for('ver_tabela'))
    
    return render_template("editar.html", nota=nota)

@app.route("/deletar_nota/<int:id>")
def deletar_nota(id):
    nota = Enfermagem.query.get(id)
    db.session.delete(nota)
    db.session.commit()

    return redirect(url_for('ver_tabela'))

if __name__ == "__main__":
    app.run(debug=True)