from flask import Flask, request
from flask_sse import sse
from flask_cors import CORS, cross_origin
from Servidor import Servidor
import json

# waitress-serve --port=5000 Aplicativo:app

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')
app.app_context().push()
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


servidor = Servidor()


@app.route('/cadastro', methods=['POST'])
@cross_origin()
def cadastro():
    corpo = request.get_json()
    nome = corpo['nome']
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
