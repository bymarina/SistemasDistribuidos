from __future__ import print_function
import Pyro4
import threading as t
from Multicast import multicast
from Enquete import Enquete
from Usuario import Usuario
from GerenciadorDeEnquetes import GerenciadorDeEnquetes
from AssinaturaDigital import AssinaturaDigital
from SupervisorEnquetePorTempo import SupervisorEnquetePorTempo


# Iniciar primeiramente o serviço de nomes: python -m Pyro4.naming

# @Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Servidor(object):
    def __init__(self):
        self.enquetes = []
        self.usuarios_cadastrados = []

        self.multicasting = multicast()

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

    def selecionar_nome_usuario(self, uri_cliente):
        nome_localizado = False
        cliente = None
        for uri_cadastrado in self.usuarios_cadastrados:
            if uri_cadastrado.uri_cliente == uri_cliente:
                nome_localizado = True
                cliente = uri_cadastrado

        if nome_localizado:
            return cliente.nome

        else:
            return None

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

    @staticmethod
    def selecionar_referencia_remota_cliente(uri_cliente):
        return Pyro4.Proxy(uri_cliente)

    @Pyro4.expose
    def menu(self, uri_cliente):
        cliente = self.selecionar_referencia_remota_cliente(uri_cliente)
        menu = (
                "\nBem vindo(a) ao serviço de enquetes, as seguintes opções estão disponíveis: " + "\n 1: Cadastrar nova enquete" + "\n 2: Consultar enquete" + "\n 3: Votar em enquete")
        cliente.mostrar_conteudo_para_cliente(menu)
        selecao = cliente.solicitar_dados("Selecionar: ")
        self.opcao(selecao, uri_cliente, cliente),

    def opcao(self, selecao, uri_cliente, cliente):
        if selecao == '1':
            self.cadastrar_enquete(uri_cliente)
        elif selecao == '2':
            self.consultar_enquete(uri_cliente)
        elif selecao == '3':
            self.votar(uri_cliente)
        elif selecao != '' and selecao is not None:
            cliente.mostrar_conteudo_para_cliente("\nOpção de menu inválida")

    @Pyro4.expose
    def cadastrar_usuario(self, uri_cliente):
        cliente = self.selecionar_referencia_remota_cliente(uri_cliente)
        nome = cliente.solicitar_dados("Digite seu nome: ")
        chave_publica = cliente.solicitar_dados("Chave")
        novo_usuario = Usuario(nome, uri_cliente, chave_publica)
        self.usuarios_cadastrados.append(novo_usuario)
        print("Novo usuário registrado: " + novo_usuario.nome)

    def cadastrar_enquete(self, uri_cliente):
        cliente = self.selecionar_referencia_remota_cliente(uri_cliente)
        dono_da_enquete = self.selecionar_nome_usuario(uri_cliente)
        cliente.mostrar_conteudo_para_cliente("\nCadastro de nova enquete: ")
        titulo = cliente.solicitar_dados("Título: ")
        local = cliente.solicitar_dados("Local: ")
        data1 = cliente.solicitar_dados("Data opção 1: ")
        horario1 = cliente.solicitar_dados("Horário: ")
        data2 = cliente.solicitar_dados("Data opção 2: ")
        horario2 = cliente.solicitar_dados("Horário: ")
        limite = cliente.solicitar_dados("Data limite da enquete (formato: AAAA-MM-DD): ")
        nova_enquete = Enquete(dono_da_enquete, titulo, local, data1, horario1, data2, horario2, limite, uri_cliente)
        self.enquetes.append(nova_enquete.pegar_dados_enquete())
        print("Nova enquete registrada: " + nova_enquete.titulo)
        self.multicasting.notificar_nova_enquete(nova_enquete)
        self.iniciar_thread_acompanhamento_validade_enquete(nova_enquete)

    @staticmethod
    def solicitar_informativo_para_votacao(objeto_enquete):
        return (
                "\nVotação: \nEnquete: " + objeto_enquete.titulo + "\nLocal: " + objeto_enquete.local + "\nData 1: " + objeto_enquete.data1 + ", Horário: " + objeto_enquete.horario1 + "\nData 2: " + objeto_enquete.data2 + ", Horário: " + objeto_enquete.horario2)

    def votar(self, uri_cliente):
        cliente = self.selecionar_referencia_remota_cliente(uri_cliente)
        nome = cliente.solicitar_dados("Digite seu nome: ")

        selecionar_usuario = self.selecionar_objeto_usuario(nome)
        if selecionar_usuario is None:
            cliente.mostrar_conteudo_para_cliente("\nUsuário não cadastrado")
            return

        nome_enquete = cliente.solicitar_dados("Nome da enquete: ")
        objeto_enquete = self.selecionar_objeto_enquete(nome_enquete)
        if objeto_enquete is None:
            cliente.mostrar_conteudo_para_cliente("\nEnquete não encontrada")
            return

        if not objeto_enquete.checar_status_enquete():
            cliente.mostrar_conteudo_para_cliente("\nEsta enquete já foi finalizada")
            return

        if objeto_enquete.checar_se_usuario_votou(nome):
            cliente.mostrar_conteudo_para_cliente("\nEste usuário já votou nesta enquete")
            return

        informacoes = self.solicitar_informativo_para_votacao(objeto_enquete)
        cliente.mostrar_conteudo_para_cliente(informacoes)
        voto = cliente.solicitar_dados("Digite 1 para selecionar a data/horario 1 ou 2 para selecionar a data/horario 2: ")
        if voto != '1' and voto != '2':
            cliente.mostrar_conteudo_para_cliente("\nOpção inválida")
            return

        objeto_enquete.votar(nome, voto)
        cliente.mostrar_conteudo_para_cliente("\nVoto registrado")
        GerenciadorDeEnquetes.tente_finalizar_enquete(objeto_enquete, self.multicasting, self.usuarios_cadastrados)

    def consultar_enquete(self, uri_cliente):
        cliente = self.selecionar_referencia_remota_cliente(uri_cliente)
        nome = cliente.solicitar_dados("Digite seu nome: ")
        nome_enquete = cliente.solicitar_dados("Nome da enquete: ")
        objeto_enquete = self.selecionar_objeto_enquete(nome_enquete)
        mensagem = cliente.solicitar_dados("Mensagem")
        assinatura = cliente.solicitar_dados("Assinatura")
        objeto_usuario = self.selecionar_objeto_usuario(nome)

        if objeto_enquete is None:
            cliente.mostrar_conteudo_para_cliente("\nEnquete não encontrada")
            return

        if not objeto_enquete.checar_se_usuario_votou(nome):
            cliente.mostrar_conteudo_para_cliente("\nPermissão negada")
            return

        if not AssinaturaDigital.verificar_assinatura(mensagem, assinatura, cliente, objeto_usuario):
            cliente.mostrar_conteudo_para_cliente("\nPermissão negada")
            return

        resultado_consulta_enquete = objeto_enquete.consultar_andamento_enquete()
        cliente.mostrar_conteudo_para_cliente(resultado_consulta_enquete)

    def iniciar_thread_acompanhamento_validade_enquete(self, objeto_enquete):
        nova_thread_acompanhamento_validade = SupervisorEnquetePorTempo(objeto_enquete, self.multicasting)

        thread_multicast = t.Thread(target=nova_thread_acompanhamento_validade.acompanhar_fechamento_enquete, args=())
        thread_multicast.daemon = True
        thread_multicast.start()
