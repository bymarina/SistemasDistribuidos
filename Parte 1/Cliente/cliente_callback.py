from __future__ import print_function
import sys
import Pyro4
import Pyro4.util
import threading as t
from Pyro4.core import Daemon
from base64 import b64encode

from assinatura_digital import assinaturaDigital

class cliente_callback(object):    

    def loopThread(self,daemon):
        daemon.requestLoop()
    
    def cadastrarUsuario(self, servidor, uri_cliente, objetoAssinatura):
        nome = input("Nome do usuário: ").strip()        
        #chave_publica = objetoAssinatura.chavePublicaBytes()
        #chave_publica_codificada = b64encode(chave_publica)
        chave_publica = objetoAssinatura.chavePublicaString()
        servidor.cadastroUsuario(nome, uri_cliente, chave_publica)
        print("O usuário foi cadastrado com sucesso: " + nome)

    def cadastrarEnquete(self, servidor, uri_cliente):
        titulo = input("Título do evento: ").strip()
        local = input("Local: ").strip()
        data1 = input("Opção 1 de data: ").strip()
        horario1 = input("Horário: ").strip()
        data2 = input("Opção 2 de data: ").strip()
        horario2 = input("Horário: ").strip()
        limite = input("Tempo de duração da enquete (em dias): ").strip()
        servidor.cadastroEnquete(titulo, local, data1, horario1, data2, horario2, limite, uri_cliente)
    
    def consultarEnquetes(self, servidor):
        enquete = input("Digite o nome da enquete a ser consultada: ").strip()
        nome = input("Digite seu nome: ").strip()
        mensagem = ("Desejo consultar esta enquete").strip()
        mensagemHash = assinaturaDigital.hashMensagem(mensagem)
        assinatura = assinaturaDigital.assinarMensagem(mensagemHash)
        print(servidor.consulta(nome, enquete, mensagem, mensagemHash, assinatura))
        

    def votarEmEnquete(self, servidor, uri_cliente, titulo):
        #titulo = input("Digite o nome da enquete que deseja votar: ").strip()
        print(servidor.informativoParaVotacao(titulo))

        print("Vote de acordo com as seguintes opções: ")
        print("1: primeira opção")
        print("2: segunda opção")
        voto = input("Seu voto: ").strip()

        servidor.votar(uri_cliente, titulo, voto)
        print("Obrigado pelo seu voto!")
        print("Resultado até o momento: " + servidor.permissaoConsulta(uri_cliente, titulo))  