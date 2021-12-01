# import Pyro4


class Notificar:
    @staticmethod
    def notificar_clientes(mensagem, lista_cadastro):
        # Enviando mensagem para usuários na lista recebida
        for cliente in lista_cadastro:
            print("Notificar")
            print(mensagem)
