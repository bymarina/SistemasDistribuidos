from datetime import date
from GerenciadorDeEnquetes import GerenciadorDeEnquetes


class SupervisorEnquetePorTempo:
    def __init__(self, objeto_enquete):
        self.objeto_enquete = objeto_enquete

    def acompanhar_fechamento_enquete(self):
        if date.today() == self.objeto_enquete.validade:
            GerenciadorDeEnquetes.finaliza_enquete(self.objeto_enquete.titulo)

