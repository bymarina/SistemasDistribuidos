from __future__ import print_function
import Pyro4
import threading as t
from Enquete import Enquete
from Usuario import Usuario
from GerenciadorDeEnquetes import GerenciadorDeEnquetes
from AssinaturaDigital import AssinaturaDigital
from SupervisorEnquetePorTempo import SupervisorEnquetePorTempo
from Notificar import Notificar
# Iniciar primeiramente o serviço de nomes: python -m Pyro4.naming


@Pyro4.behavior(instance_mode="single")
class Servidor(object):
    def __init__(self):
        self.enquetes = []
        self.usuarios_cadastrados = []

    def selecionar_objeto_enquete(self, titulo):
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
        for usuario in self.usuarios_cadastrados:
            if usuario.nome == nome:
                return True
        else:
            return False

    def selecionar_objeto_usuario(self, nome):
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

    @Pyro4.expose
    def cadastrar_usuario(self, uri_cliente, nome, chave_publica):
        novo_usuario = Usuario(nome, uri_cliente, chave_publica)
        self.usuarios_cadastrados.append(novo_usuario)
        return "Novo usuário registrado: " + novo_usuario.nome

    @Pyro4.expose
    def cadastrar_enquete(self, nome, titulo, local, data1, horario1, data2, horario2, limite):
        if not self.verificar_cadastro_de_usuario(nome):
            return "\nUsuário não cadastrado"

        nova_enquete = Enquete(nome, titulo, local, data1, horario1, data2, horario2, limite)
        self.enquetes.append(nova_enquete)

        notificacao = ("\nPor gentileza votar na nova enquete criada: " + titulo)
        Notificar.notificar_clientes(notificacao, self.usuarios_cadastrados)
        self.iniciar_thread_acompanhamento_validade_enquete(nova_enquete)

        return "\nEnquete registrada"

    @Pyro4.expose
    def solicitar_informativo_para_votacao(self, titulo):
        objeto_enquete = self.selecionar_objeto_enquete(titulo)
        if not objeto_enquete.checar_status_enquete():
            return "\nEsta enquete já foi finalizada"
        informativo = objeto_enquete.informar_dados_para_votar()
        return informativo

    @Pyro4.expose
    def votar(self, nome, titulo, voto):
        objeto_enquete = self.selecionar_objeto_enquete(titulo)

        if not self.verificar_cadastro_de_usuario(nome):
            return "\nUsuário não cadastrado"

        if objeto_enquete is None:
            return "\nEnquete não encontrada"

        if not objeto_enquete.checar_status_enquete():
            return "\nEsta enquete já foi finalizada"

        if objeto_enquete.checar_se_usuario_votou(nome):
            return "\nEste usuário já votou nesta enquete"

        if voto != '1' and voto != '2':
            return "\nOpção inválida"

        objeto_enquete.votar(nome, voto)
        GerenciadorDeEnquetes.tente_finalizar_enquete(objeto_enquete, self.usuarios_cadastrados)

        return "\nVoto registrado"

    @Pyro4.expose
    def consultar_enquete(self, nome, titulo, mensagem, assinatura_digital):
        objeto_enquete = self.selecionar_objeto_enquete(titulo)
        objeto_usuario = self.selecionar_objeto_usuario(nome)

        if objeto_enquete is None:
            return "\nEnquete não encontrada"

        if not objeto_enquete.checar_status_enquete():
            return "\nEsta enquete já foi finalizada"

        if not objeto_enquete.checar_se_usuario_votou(nome):
            return "\nPermissão negada"

        if not AssinaturaDigital.verificar_assinatura(mensagem, assinatura_digital, objeto_usuario):
            return "\"nPermissão negada"

        resultado_consulta_enquete = objeto_enquete.consultar_andamento_enquete()
        return resultado_consulta_enquete

    def iniciar_thread_acompanhamento_validade_enquete(self, objeto_enquete):
        nova_thread_acompanhamento_validade = SupervisorEnquetePorTempo(objeto_enquete, self.usuarios_cadastrados)

        thread_multicast = t.Thread(target=nova_thread_acompanhamento_validade.acompanhar_fechamento_enquete, args=())
        thread_multicast.daemon = True
        thread_multicast.start()
