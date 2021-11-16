from __future__ import print_function
from Crypto.Hash import SHA256
import Pyro4
from _thread import *
from usuario import usuario
from multicast import multicast
from enquete import enquete
from usuario import usuario
from base64 import b64decode, b64encode

#Iniciar primeiramente o serviço de nomes: python -m Pyro4.naming

@Pyro4.expose
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


    def cadastroUsuario(self, nome, uri_cliente, chave_publica):
        novo_usuario = usuario(nome, uri_cliente, chave_publica)
        self.usuarios.append(novo_usuario)       
        print("Novo usuário registrado: " + novo_usuario.nome)
    
    def cadastroEnquete(self, titulo, local, data1, horario1, data2, horario2, limite, uri_cliente):
        nome = self.selecionaNomeUsuario(uri_cliente)
        nova_enquete = enquete(nome, titulo, local, data1, horario1, data2, horario2, limite, uri_cliente)
        self.enquetes.append(nova_enquete.dadosEnquete())
        print("Nova enquete registrada: " + nova_enquete.titulo)
        self.multicasting.notificarNovaEnquete(nova_enquete)

    def informativoParaVotacao(self, titulo):
        enquete = self.selecionaObjetoEnquete(titulo)
        if enquete == False:
            return ("Enquete não encontrada")
        else:
            return ("Opção 1: " + enquete.data1 + " , " + "Opção 2: " + enquete.data2)

    def votar(self, uri_cliente, titulo, voto):
        enquete = self.selecionaObjetoEnquete(titulo)
        nome = self.selecionaNomeUsuario(uri_cliente)

        if nome != False:
            if enquete == False:
                return ("Enquete não encontrada")
            
            elif enquete.checarEnqueteAtiva(titulo) == True:
                enquete.votar(nome, voto) 
                return ("Voto registrado")

            else:  
                return ("Esta enquete não está mais ativa")             
            
        else:
            return ("Usuário não cadastrado")


    def consulta(self, nome, titulo, mensagem, mensagemHash, assinatura):
        enquete = self.selecionaObjetoEnquete(titulo) 

        if enquete != False:
            if self.verificaAssinatura(nome, mensagem, mensagemHash, assinatura) == True:
                return enquete.consultaResultado()
            else:
                return ("Permissão negada")                   
        else:
            return("Enquete não localizada") 

    def verificaAssinatura(self, nome, mensagem, mensagemHash, assinatura):
        usuario = self.selecionaObjetoUsuario(nome)
        chave_publica = usuario.retorna_chave_publica()
        if usuario != False:
            mensagemHashVerificar = SHA256.new(mensagem.encode('utf-8')).digest()
            if(chave_publica.verify(mensagemHashVerificar, assinatura)):
                return True
            else:
                return False
        else:
            print("Erro na verificação da assinatura digital")
            return False

    def finalizarEnquete(self, titulo):
        enquete = self.selecionaObjetoEnquete(titulo) 
        if enquete != False:
            enquete.finalizarEnquete(titulo)
        else:
            print("Falha na finalização da enquete: " + titulo)