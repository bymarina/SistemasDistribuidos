from __future__ import print_function
import Pyro4.util


@Pyro4.expose
class ClienteCallback(object):
    @staticmethod
    def loop_thread(daemon):
        daemon.requestLoop()

    def referenciar_assinatura_digital(self, assinatura):
        self.chave_publica = assinatura.chave_publica_string()
        self.objetoAssinaturaDigital = assinatura
        self.mensagem = "Desejo consultar esta enquete"
        self.assinaturaDigital = assinatura.assinar_mensagem(self.mensagem)

    @staticmethod
    def mostrar_conteudo_para_cliente(conteudo):
        print(conteudo)

    def solicitar_dados(self, solicitar):
        if solicitar == "Chave":
            return self.chave_publica
        elif solicitar == "Mensagem":
            return self.mensagem
        elif solicitar == "Assinatura":
            return self.assinaturaDigital
        else:
            dado = input(solicitar).strip()
            return dado

    def cadastrar_usuario(self, servidor, uri_cliente):
        servidor.cadastrar_usuario(uri_cliente)
        self.servidor = servidor
