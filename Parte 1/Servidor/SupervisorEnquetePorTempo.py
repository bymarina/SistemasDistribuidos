from datetime import date
from GerenciadorDeEnquetes import GerenciadorDeEnquetes


class SupervisorEnquetePorTempo:
    def __init__(self, objeto_enquete, objeto_multicast):
        self.objeto_enquete = objeto_enquete
        self.objeto_multicast = objeto_multicast

    def acompanhar_fechamento_enquete(self):
        data_atual = date.today()
        data_atual_string = data_atual.strftime("%Y-%m-%d")
        if data_atual_string == self.objeto_enquete.limite:
            GerenciadorDeEnquetes.finalizar_enquete(self.objeto_enquete, self.objeto_multicast)

