from datetime import date
from GerenciadorDeEnquetes import GerenciadorDeEnquetes


class SupervisorEnquetePorTempo:
    def __init__(self, objeto_enquete, lista_usuarios_cadastro):
        self.objeto_enquete = objeto_enquete
        self.lista_usuarios_cadastro = lista_usuarios_cadastro

    def acompanhar_fechamento_enquete(self):
        data_atual = date.today()
        validade = self.objeto_enquete.limite
        validade_ano = int(validade[0:4])
        validade_mes = int(validade[5:7])
        validade_dia = int(validade[8:])
        data_validade = date(validade_ano, validade_mes, validade_dia)

        if data_atual >= data_validade:
            GerenciadorDeEnquetes.finalizar_enquete(self.objeto_enquete, self.lista_usuarios_cadastro)

