from __future__ import print_function
import threading as t
from Enquete import Enquete
from Usuario import Usuario
from GerenciadorDeEnquetes import GerenciadorDeEnquetes
from SupervisorEnquetePorTempo import SupervisorEnquetePorTempo
from GerenciadorMensagensSubscribers import GerenciadorMensagens


class Servidor(object):
    def __init__(self):
        self.enquetes = []
        self.usuarios_cadastrados = []
        self.gerenciadores_de_mensagens = []

    def selecionar_objeto_enquete(self, titulo):
        # Selecionando um objeto enquete a partir de seu título
        enquete_encontrada = False
        objeto_enquete = None
        for enquete_cadastrada in self.enquetes:
            if enquete_cadastrada.titulo == titulo:
                objeto_enquete = enquete_cadastrada
                enquete_encontrada = True

        if enquete_encontrada:
            return objeto_enquete

        else:
            return None

    def verificar_cadastro_de_usuario(self, nome):
        # Verificando se usuário já foi cadastrado
        for usuario in self.usuarios_cadastrados:
            if usuario.nome == nome:
                return True
        else:
            return False

    def selecionar_objeto_usuario(self, nome):
        # Selecionando um objeto usuário a partir de seu nome
        usuario_localizado = False
        objeto_usuario = None
        for nomes_cadastrados in self.usuarios_cadastrados:
            if nomes_cadastrados.nome == nome:
                usuario_localizado = True
                objeto_usuario = nomes_cadastrados

        if usuario_localizado:
            return objeto_usuario

        else:
            return None

    def selecionar_gerenciador_de_mensagens(self, objeto_enquete):
        # Selecionando um objeto gerenciador de mensagens a partir de sua enquete
        gerenciador_localizado = False
        objeto_gerenciador = None
        for gerenciador in self.gerenciadores_de_mensagens:
            if gerenciador.objeto_enquete == objeto_enquete:
                gerenciador_localizado = True
                objeto_gerenciador = gerenciador

        if gerenciador_localizado:
            return objeto_gerenciador

        else:
            return None

    def cadastrar_usuario(self, nome):
        # Criação do usuário:
        novo_usuario = Usuario(nome)
        self.usuarios_cadastrados.append(novo_usuario)
        return "Novo usuário registrado: " + novo_usuario.nome

    def cadastrar_enquete(self, nome, titulo, local, data1, horario1, data2, horario2, limite):
        if not self.verificar_cadastro_de_usuario(nome):
            return "\nUsuário não cadastrado"

        # Criação da enquete:
        nova_enquete = Enquete(nome, titulo, local, data1, horario1, data2, horario2, limite)
        self.enquetes.append(nova_enquete)

        # O gerenciador de mensagens é onde são armazenadas as informações de subscribers de cada enquete
        # O gerenciador de mensagens também ativa o envio de notificações do servidor para os subscribers
        # Criando o gerenciador de mensagens:
        gerenciador_de_mensagens = GerenciadorMensagens(nova_enquete)
        self.gerenciadores_de_mensagens.append(gerenciador_de_mensagens)

        # Adicionando o criador na enquete como subscriber:
        criador_enquete = self.selecionar_objeto_usuario(nome)
        gerenciador_de_mensagens.adicionar_subscriber_criador(criador_enquete)

        # Notificando a criação de uma nova enquete:
        gerenciador_de_mensagens.notificar_nova_enquete(self.usuarios_cadastrados)

        # Iniciando a thread que acompanha o encerramento de uma enquete por data limite
        self.iniciar_thread_acompanhamento_validade_enquete(nova_enquete, gerenciador_de_mensagens)

        return "\nEnquete registrada"

    def solicitar_informativo_para_votacao(self, titulo):
        # O informativo para votação é uma mensagem que mostra todas as informações que o votante precisa sobre a enquete
        objeto_enquete = self.selecionar_objeto_enquete(titulo)
        if not objeto_enquete.checar_status_enquete():
            return "\nEsta enquete já foi finalizada"
        informativo = objeto_enquete.informar_dados_para_votar()
        return informativo

    def votar(self, nome, titulo, voto):
        objeto_enquete = self.selecionar_objeto_enquete(titulo)

        # Verificando se o usuário que deseja votar possui cadastro
        if not self.verificar_cadastro_de_usuario(nome):
            return "\nUsuário não cadastrado"

        # Verificando se a enquete solicitada existe
        if objeto_enquete is None:
            return "\nEnquete não encontrada"

        # Verificando se a enquete solicitada está em andamento ou se já foi encerrada
        if not objeto_enquete.checar_status_enquete():
            return "\nEsta enquete já foi finalizada"

        # Verificando se o usuário solicitante já votou nesta enquete
        if objeto_enquete.checar_se_usuario_votou(nome):
            return "\nEste usuário já votou nesta enquete"

        # Verificando se a opção de voto é válida
        if voto != '1' and voto != '2':
            return "\nOpção inválida"

        # Registrando o voto
        objeto_enquete.votar(nome, voto)

        # Adicionando o votante à lista de subscribers dessa enquete
        votante = self.selecionar_objeto_usuario(nome)
        gerenciador_de_mensagens = self.selecionar_gerenciador_de_mensagens(objeto_enquete)
        gerenciador_de_mensagens.adicionar_subscriber_votante(votante)

        # Verificando se já é possível finalizar a enquete por votos
        GerenciadorDeEnquetes.tente_finalizar_enquete(objeto_enquete, self.usuarios_cadastrados, gerenciador_de_mensagens)

        return "\nVoto registrado"

    def consultar_enquete(self, nome, titulo):
        objeto_enquete = self.selecionar_objeto_enquete(titulo)
        objeto_usuario = self.selecionar_objeto_usuario(nome)

        # Verificando se a enquete existe
        if objeto_enquete is None:
            return "\nEnquete não encontrada"

        # Verificando se o usuário participa da enquete como votante
        if not objeto_enquete.checar_se_usuario_votou(nome):
            return "\nPermissão negada"

        # Disponibilizando o informativo sobre andamento da enquete
        resultado_consulta_enquete = objeto_enquete.consultar_andamento_enquete()
        return resultado_consulta_enquete

    @staticmethod
    def iniciar_thread_acompanhamento_validade_enquete(objeto_enquete, gerenciador_de_mensagens):
        # Criando a thread que acompanha se uma enquete deve ser finalizada por limite de data atingido
        nova_thread_acompanhamento_validade = SupervisorEnquetePorTempo(objeto_enquete, gerenciador_de_mensagens)

        thread_multicast = t.Thread(target=nova_thread_acompanhamento_validade.acompanhar_fechamento_enquete, args=())
        thread_multicast.daemon = True
        thread_multicast.start()
