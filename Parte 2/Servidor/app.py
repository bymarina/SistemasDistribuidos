from flask import Flask, request
import json
from Servidor import Servidor

app = Flask(__name__)

servidor = Servidor()


@app.route('/')  # Configurando para a rota: http://localhost:5000/ que é a default
def hello_world():
    return 'Hello World'


@app.route('/cadastro', methods=['POST'])
def cadastro():
    corpo = request.get_json()
    nome = corpo['nome']
    print(nome)
    print(type(nome))
    retorno_servidor = servidor.cadastrar_usuario(nome)
    resposta = {"status": 200,
                "message": retorno_servidor}
    return json.dumps(resposta)


@app.route('/novaenquete', methods=['POST'])
def nova_enquete():
    corpo = request.get_json()
    nome = corpo['nome']
    titulo = corpo['titulo']
    local = corpo['local']
    data1 = corpo['data1']
    horario1 = corpo['horario1']
    data2 = corpo['data2']
    horario2 = corpo['horario2']
    limite = corpo['limite']
    retorno_servidor = servidor.cadastrar_enquete(nome, titulo, local, data1, horario1, data2, horario2, limite)
    resposta = {"status": 200,
                "message": retorno_servidor}
    return json.dumps(resposta)


@app.route('/consultaenquete', methods=['POST'])
def consultar_enquete():
    corpo = request.get_json()
    nome = corpo['nome']
    titulo = corpo['titulo']
    retorno_servidor = servidor.consultar_enquete(nome, titulo)
    resposta = {"status": 200,
                "message": retorno_servidor}
    return json.dumps(resposta)


@app.route('/votar', methods=['POST'])
def votar_enquete():
    corpo = request.get_json()
    nome = corpo['nome']
    titulo = corpo['titulo']
    voto = corpo['voto']
    retorno_servidor = servidor.votar(nome, titulo, voto)
    resposta = {"status": 200,
                "message": retorno_servidor}
    return json.dumps(resposta)

