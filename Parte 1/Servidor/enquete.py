from multicast import multicast

class enquete:
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


    def checagemUsuario(self, nome):
        usuarioPresente = False
        for x in self.votosOpcao1:
            if x == nome:
                usuarioPresente = True
        for y in self.votosOpcao2:
            if y == nome:
                usuarioPresente = True

        return usuarioPresente

    def votar(self, nome, voto):            
        if voto == '1':
            self.votosOpcao1.append(nome)
        elif voto == '2':
            self.votosOpcao2.append(nome)

    def consultaResultado(self):
        contagemOpcao1 = str(len(self.votosOpcao1))
        contagemOpcao2 = str(len(self.votosOpcao2))

        if contagemOpcao1 > contagemOpcao2:
            frase = ("Opção 1 com mais votos. " + "Data: " + self.data1 + ", Horario: "+ self.horario1 +" no local: " + self.local + "\nTotal de votos na opção 1: " + contagemOpcao1 + "\nTotal de votos na opção 2: " + contagemOpcao2)
            return frase
        elif contagemOpcao1 < contagemOpcao2:
            frase = ("Opção 2 com mais votos. " + "Data: " + self.data2 + ", Horario: "+ self.horario2 +" no local: " + self.local + "\nTotal de votos na opção 1: " + contagemOpcao1 + "\nTotal de votos na opção 2: " + contagemOpcao2)
            return frase
        elif (contagemOpcao1 ==0) and (contagemOpcao2 == 0):
            frase = ("Nenhum voto registrado.")
            return frase
        else:
            frase = ("Empate!" + "Total de votos na opção 1: " + contagemOpcao1 + ", total de votos na opção 2: " + contagemOpcao2)
            return frase

    def finalizarEnquete(self, nome):
        if self.nome == nome:
            self.enqueteAtiva = False
            multicast.notificarEnqueteFinalizada(self)
            return ("Enquete: " + self.titulo + " " + "finalizada!")

        else:
            return ("Somente o criador da enquete pode finalizá-la")

    def dadosEnquete(self):
        return self

    def checarEnqueteAtiva(self):
        return self.enqueteAtiva