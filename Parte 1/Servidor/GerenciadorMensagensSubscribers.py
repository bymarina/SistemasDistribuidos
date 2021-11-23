from Notificar import Notificar


class GerenciadorMensagens(object):
    def __init__(self, objeto_enquete):
        self.objeto_enquete = objeto_enquete

        self.mensagem_nova_enquete = ("\nPor gentileza votar na nova enquete criada: " + objeto_enquete.titulo + objeto_enquete.informar_dados_para_votar())
        self.mensagem_criador_enquete_finalizada = ("\nA seguinte enquete criada por você foi finalizada: " + objeto_enquete.titulo)

        self.subscriber_criador = []
        self.subscribers_votantes = []

    def adicionar_subscriber_criador(self, criador):
        # Adicionando criador da enquete à lista de subscriber de criador de enquete
        self.subscriber_criador.append(criador)

    def adicionar_subscriber_votante(self, votante):
        # Adicionando votantes à lista de subscribers
        self.subscribers_votantes.append(votante)

    def notificar_nova_enquete(self, lista_usuarios_cadastrados):
        # Solicitando envio de notificação de nova enquete criada para todos os usuários
        Notificar.notificar_clientes(self.mensagem_nova_enquete, lista_usuarios_cadastrados)

    def notificar_criador_enquete_finalizada(self):
        # Solicitando envio de notificação de enquete encerrada especial para o criador da enquete
        Notificar.notificar_clientes(self.mensagem_criador_enquete_finalizada, self.subscriber_criador)

    def notificar_votantes_enquete_finalizada(self):
        # Solicitando envio de notificação de enquete encerrada para os votantes da enquete
        resultado_enquete = self.objeto_enquete.consultar_resultado()
        mensagem_votantes_enquete_finalizada = ("\nA seguinte enquete foi finalizada: " + self.objeto_enquete.titulo + "\n" + resultado_enquete)
        Notificar.notificar_clientes(mensagem_votantes_enquete_finalizada, self.subscribers_votantes)

