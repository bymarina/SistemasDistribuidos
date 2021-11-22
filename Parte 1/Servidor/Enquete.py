from datetime import date
from datetime import timedelta


class Enquete:
    def __init__(self, nome, titulo, local, data1, horario1, data2, horario2, limite, uri_cliente):
        self.nome = nome
        self.titulo = titulo
        self.local = local
        self.data1 = data1
        self.horario1 = horario1
        self.data2 = data2
        self.horario2 = horario2
        self.limite = limite
        self.uri_cliente = uri_cliente
        self.enqueteAtiva = True
        self.votosOpcao1 = []
        self.votosOpcao2 = []
        self.validade = Enquete.calcular_validade_enquete(self.limite)

    @staticmethod
    def calcular_validade_enquete(limite):
        data_de_hoje = date.today()
        limite_int = int(limite)
        validade_enquete = data_de_hoje + timedelta(days=limite_int)
        return validade_enquete

    def checar_status_enquete(self):
        return self.enqueteAtiva

    def checar_se_usuario_votou(self, nome):
        votantes = self.votosOpcao1 + self.votosOpcao2
        for nome_votante in votantes:
            if nome_votante == nome:
                return True
        return False

    def votar(self, nome, voto):
        if voto == '1':
            self.votosOpcao1.append(nome)
        elif voto == '2':
            self.votosOpcao2.append(nome)

    def consultar_andamento_enquete(self):
        contagem_opcao1 = str(len(self.votosOpcao1))
        contagem_opcao2 = str(len(self.votosOpcao2))
        usuarios_ja_votaram = str(self.votosOpcao1 + self.votosOpcao2)

        if contagem_opcao1 > contagem_opcao2:
            frase = (
                        "Opção 1 com mais votos. " + "Data: " + self.data1 + ", Horário: " + self.horario1 + " no local: " + self.local + "\nTotal de votos na opção 1: " + contagem_opcao1 + "\nTotal de votos na opção 2: " + contagem_opcao2 + "\nParticipantes que votaram: " + usuarios_ja_votaram)
            return frase
        elif contagem_opcao1 < contagem_opcao2:
            frase = (
                        "Opção 2 com mais votos. " + "Data: " + self.data2 + ", Horário: " + self.horario2 + " no local: " + self.local + "\nTotal de votos na opção 1: " + contagem_opcao1 + "\nTotal de votos na opção 2: " + contagem_opcao2 + "\nParticipantes que votaram: " + usuarios_ja_votaram)
            return frase
        elif (contagem_opcao1 == 0) and (contagem_opcao2 == 0):
            frase = "Nenhum voto registrado."
            return frase
        else:
            frase = (
                        "Empate!" + "Total de votos na opção 1: " + contagem_opcao1 + ", total de votos na opção 2: " + contagem_opcao2 + contagem_opcao2 + "\nParticipantes que votaram: " + usuarios_ja_votaram)
            return frase

    def consultar_resultado(self):
        contagem_opcao1 = str(len(self.votosOpcao1))
        contagem_opcao2 = str(len(self.votosOpcao2))

        if contagem_opcao1 > contagem_opcao2:
            frase = ("A opção 1 foi escolhida pela maioria dos votantes. Local: " + self.local + " Data: " + self.data1 + " Horário: " + self.horario1)
        elif contagem_opcao2 > contagem_opcao1:
            frase = ("A opção 2 foi escolhida pela maioria dos votantes. Local: " + self.local + " Data: " + self.data2 + " Horário: " + self.horario2)
        elif contagem_opcao1 == contagem_opcao2:
            frase = "A votação resultou em empate."
        elif contagem_opcao2 == 0 and contagem_opcao2 == 0:
            frase = "Nenhum usuário votou nesta enquete"
        else:
            frase = "Os resultados ainda são inconclusivos"
        return frase

    def finalizar_enquete_por_votos(self):
        self.enqueteAtiva = False
        print("Enquete finalizada: " + self.titulo)

    def pegar_dados_enquete(self):
        return self
