from __future__ import print_function
import Pyro4
import Pyro4.util


@Pyro4.expose

class cliente_callback(object): 
    def loopThread(self,daemon):
        daemon.requestLoop()

    def referenciaAssinaturaDigital(self, assinatura):
        self.chave_publica = assinatura.chavePublicaString()
        self.objetoAssinaturaDigital = assinatura
        self.mensagem = "Desejo consultar esta enquete"
        self.assinaturaDigital = assinatura.assinarMensagem(self.mensagem)

    def mostrarConteudo(self, conteudo):
        print(conteudo)

    def solicitarDados(self, solicitar):
        if solicitar == "Chave":
            return self.chave_publica
        elif solicitar == "Mensagem":
            return self.mensagem
        elif solicitar == "Assinatura":
            return self.assinaturaDigital
        else:
            dado = input(solicitar).strip()
            return dado        
    
    def cadastrarUsuario(self, servidor, uri_cliente):
        servidor.cadastroUsuario(uri_cliente)
        self.servidor = servidor