from __future__ import print_function
import Pyro4.util


@Pyro4.expose
class ClienteCallback(object):
    @staticmethod
    # Esperar comunicação
    def loop_thread(daemon):
        daemon.requestLoop()

    @staticmethod
    # Exibir notificações recebidas do servidor
    def mostrar_notificacoes(notificacao):
        print(notificacao)
