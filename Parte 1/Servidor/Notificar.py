import Pyro4


class Notificar:
    @staticmethod
    def notificar_clientes(mensagem, lista_cadastro):
        for cliente in lista_cadastro:
            referencia_cliente = Pyro4.Proxy(cliente.uri_cliente)
            referencia_cliente.mostrar_notificacoes(mensagem)
