from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Nota
from datetime import datetime
import json
import pysnooper

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with open('C:/Users/Positivo/Enfermagem_app/data/terminologias.json') as f:
    terminologias = json.load(f)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    notas = Nota.query.all()
    for nota in notas:
        print(f"id: {nota.id}, nome: {nota.nome_paciente}")
    return render_template('index.html')

@app.route("/ver_tebela")
def ver_tabela():
    notas = Nota.query.all()
    return render_template("tabela.html", notas=notas)

@app.route('/adicionar', methods=['POST'])
@pysnooper.snoop()
def adicionar_nota():
    data_hora = datetime.strptime(request.form['data_hora'], '%Y-%m-%dT%H:%M')
    descricao_paciente = request.form['descricao_paciente']
    terminologia = request.form['terminologia']
    sinais_vitais = request.form['sinais_vitais']
    nome_paciente = request.form['nome_paciente']
    nome_enfermeiro = request.form['nome_enfermeiro']
    
    nova_nota = Nota(
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


@app.route("/deletar_nota/<int:id>")
@pysnooper.snoop()
def deletar_nota(id):
    nota = Nota.query.get(id)
    db.session.delete(nota)
    db.session.commit()
    print(f"id: {nota.id} excluido com sucesso!")
    return redirect(url_for('ver_tabela'))

if __name__=="__main__":
    app.run(debug=True)