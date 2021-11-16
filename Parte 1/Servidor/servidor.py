from __future__ import print_function
from Crypto.Hash import SHA256
import Pyro4
from _thread import *

from usuario import usuario
from multicast import multicast
from enquete import enquete
from usuario import usuario

#Iniciar primeiramente o serviço de nomes: python -m Pyro4.naming

#@Pyro4.expose
@Pyro4.behavior(instance_mode="single")

class servidor(object):
    def __init__(self):
        self.enquetes = []
        self.usuarios = []

        self.multicasting = multicast()

    def selecionaObjetoEnquete(self, titulo):
        enqueteEncontrada = False
        for x in self.enquetes:
            if x.titulo == titulo:
                enquete = x
                enqueteEncontrada = True

        if enqueteEncontrada == True:
            return enquete

        else:
            return False

    def selecionaNomeUsuario(self, uri_cliente):
        nomeLocalizado = False
        for x in self.usuarios:
            if x.uri_cliente == uri_cliente:
                nomeLocalizado = True
                cliente = x
        
        if nomeLocalizado == True:
            return cliente.nome

        else:
            return False

    def selecionaObjetoUsuario(self, nome):
        usuarioLocalizado = False
        for x in self.usuarios:
            if x.nome == nome:
                usuarioLocalizado = True
                objetoUsuario = x
        
        if usuarioLocalizado == True:
            return objetoUsuario
        
        else:
            return False

    def selecionaReferenciaRemotaCliente(self, uri_cliente):
        return Pyro4.Proxy(uri_cliente)    

    @Pyro4.expose    
    def menu(self, uri_cliente):     
        cliente = self.selecionaReferenciaRemotaCliente(uri_cliente)   
        menu =  ("Bem vindo(a) ao serviço de enquetes, as seguintes opções estão disponíveis: " + "\n 1: Cadastrar nova enquete" + "\n 2: Consultar enquete" + "\n 3: Votar em enquete")
        cliente.mostrarConteudo(menu)
        selecao = cliente.solicitarDados("Selecionar: ")
        opcaoSelecionada = self.opcao(selecao, uri_cliente)
        if opcaoSelecionada == False:
            cliente.mostrarConteudo("Opção inválida")

    def opcao(self, selecao, uri_cliente):
        if selecao == '1':
            self.cadastroEnquete(uri_cliente)
        elif selecao == '2':
            self.consulta(uri_cliente)
        elif selecao == '3':
            self.votar(uri_cliente)
        else:
            return False

    @Pyro4.expose
    def cadastroUsuario(self, uri_cliente):
        cliente = self.selecionaReferenciaRemotaCliente(uri_cliente)
        nome = cliente.solicitarDados("Digite seu nome: ")
        chave_publica = cliente.solicitarDados("Chave")
        novo_usuario = usuario(nome, uri_cliente, chave_publica)
        self.usuarios.append(novo_usuario)       
        print("Novo usuário registrado: " + novo_usuario.nome)
    
    def cadastroEnquete(self, uri_cliente):
        cliente = self.selecionaReferenciaRemotaCliente(uri_cliente)
        donoDaEnquete = self.selecionaNomeUsuario(uri_cliente)
        titulo = cliente.solicitarDados("Título: ")
        local = cliente.solicitarDados("Local: ")
        data1 = cliente.solicitarDados("Data opção 1: ")
        horario1 = cliente.solicitarDados("Horário: ")
        data2 = cliente.solicitarDados("Data opção 2: ")
        horario2 = cliente.solicitarDados("Horário: ")
        limite = cliente.solicitarDados("Tempo de duração da enquete (em dias): ")
        nova_enquete = enquete(donoDaEnquete, titulo, local, data1, horario1, data2, horario2, limite, uri_cliente)
        self.enquetes.append(nova_enquete.dadosEnquete())
        print("Nova enquete registrada: " + nova_enquete.titulo)
        self.multicasting.notificarNovaEnquete(nova_enquete)

    def informativoParaVotacao(self, titulo):
        enquete = self.selecionaObjetoEnquete(titulo)
        if enquete == False:
            return ("Enquete não encontrada")
        else:
            return ("Opção 1: " + enquete.data1 + " , " + "Opção 2: " + enquete.data2)

    
    def votar(self, uri_cliente):        
        cliente = self.selecionaReferenciaRemotaCliente(uri_cliente)

        nome = cliente.solicitarDados("Digite seu nome: ")
        selecionarUsuario = self.selecionaObjetoUsuario(nome)
        if selecionarUsuario == False:
            cliente.mostrarConteudo("Usuário não cadastrado")
        else:
            nomeEnquete = cliente.solicitarDados("Nome da enquete: ")
            selecionarEnquete = self.selecionaObjetoEnquete(nomeEnquete)
            if selecionarEnquete == False:
                cliente.mostrarConteudo("Enquete não encontrada")
            else:
                voto = cliente.solicitarDados("Digite 1 para selecionar a opção 1 ou 2 para selecionar a opção 2: ")
                if voto != '1' and voto != '2':
                    cliente.mostrarConteudo("Opção inválida")
                else: 
                    resultadoVoto = selecionarEnquete.votar(nome, voto)
                    if resultadoVoto == True:
                        cliente.mostrarConteudo("Voto registrado")
                    else:
                        cliente.mostrarConteudo("Este usuário já votou nesta enquete")

    def consulta(self, uri_cliente):
        cliente = self.selecionaReferenciaRemotaCliente(uri_cliente)
        nome = cliente.solicitarDados("Digite seu nome: ")
        enquete = cliente.solicitarDados("Nome da enquete: ") 
        objetoEnquete = self.selecionaObjetoEnquete(enquete)
        mensagem = cliente.solicitarDados("Mensagem")
        assinatura = cliente.solicitarDados("Assinatura")

        if objetoEnquete != False:
            if self.verificaAssinatura(nome, mensagem, assinatura, cliente) == True:
                resultadoConsulta = objetoEnquete.consultaResultado()
                cliente.mostrarConteudo(resultadoConsulta)
            else:
                cliente.mostrarConteudo("Permissão negada")                  
        else:
            cliente.mostrarConteudo("Enquete não encontrada") 

    def verificaAssinatura(self, nome, mensagem, assinatura, cliente):
        usuario = self.selecionaObjetoUsuario(nome)
        chave_publica = usuario.retorna_chave_publica()

        if usuario == False:
            cliente.mostrarConteudo("Erro na localização do usuário")
        else:
            mensagemHash = SHA256.new(mensagem.encode('utf-8')).digest()
            if(chave_publica.verify(mensagemHash, assinatura)):
                return True
            else:
                return False

    def finalizarEnquete(self, titulo):
        enquete = self.selecionaObjetoEnquete(titulo) 
        if enquete != False:
            enquete.finalizarEnquete(titulo)
        else:
            print("Falha na finalização da enquete: " + titulo)
