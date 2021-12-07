from flask_sse import sse


class Notificar:
    @staticmethod
    def notificar_clientes(mensagem, lista_usuarios):
        for usuario in lista_usuarios:
            sse.publish({"message": mensagem, "data": None}, type=usuario.nome)
