from datetime import date
from GerenciadorDeEnquetes import GerenciadorDeEnquetes


class SupervisorEnquetePorTempo:
    def __init__(self, objeto_enquete, gerenciador_de_mensagens):
        self.objeto_enquete = objeto_enquete
        self.gerenciador_de_mensagens = gerenciador_de_mensagens

    def acompanhar_fechamento_enquete(self):
        # Pegando data de hoje:
        data_atual = date.today()

        # Transformando a data limite recebida em formato de data para poder realizar comparações
        validade = self.objeto_enquete.limite
        validade_ano = int(validade[0:4])
        validade_mes = int(validade[5:7])
        validade_dia = int(validade[8:])
        data_validade = date(validade_ano, validade_mes, validade_dia)

        # Verificando validade
        if data_atual >= data_validade:
            # Solicitando encerramento da enquete por validade
            GerenciadorDeEnquetes.finalizar_enquete(self.objeto_enquete, self.gerenciador_de_mensagens)

