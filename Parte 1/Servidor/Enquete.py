class Enquete:
    def __init__(self, criador, titulo, local, data1, horario1, data2, horario2, limite):
        self.criador = criador
        self.titulo = titulo
        self.local = local
        self.data1 = data1
        self.horario1 = horario1
        self.data2 = data2
        self.horario2 = horario2
        self.limite = limite
        self.enqueteAtiva = True

        self.votosOpcao1 = []
        self.votosOpcao2 = []

    def checar_status_enquete(self):
        # Retorna se a enquete está ativa ou se foi encerrada
        return self.enqueteAtiva

    def checar_se_usuario_votou(self, nome):
        # Checando se o usuário corresponde ao nome recebido já votou
        votantes = self.votosOpcao1 + self.votosOpcao2
        for nome_votante in votantes:
            if nome_votante == nome:
                return True
        return False

    def retornar_todos_os_votantes(self):
        # Retornando lista de todos os votantes
        votantes = self.votosOpcao1 + self.votosOpcao2
        return votantes

    def informar_dados_para_votar(self):
        # Retornando mensagem informativa com dados da enquete para votação
        return "\nVotação: \nEnquete: " + self.titulo + "\nLocal: " + self.local + "\nData 1: " + self.data1 + ", Horário: " + self.horario1 + "\nData 2: " + self.data2 + ", Horário: " + self.horario2

    def votar(self, nome, voto):
        # Contabilizando votos
        if voto == '1':
            self.votosOpcao1.append(nome)
        elif voto == '2':
            self.votosOpcao2.append(nome)

    def consultar_andamento_enquete(self):
        # Retorna o estado atual da enquete
        # Retorna também qual opção está ganhando e informações sobre esta opção
        # Retorna quais usuários já votaram na enquete
        contagem_opcao1 = str(len(self.votosOpcao1))
        contagem_opcao2 = str(len(self.votosOpcao2))
        usuarios_ja_votaram = str(self.votosOpcao1 + self.votosOpcao2)

        # Verifica estado
        estado = "\nEnquete em andamento."
        if not self.enqueteAtiva:
            estado = "\nEnquete encerrada."

        # Verifica qual opção está ganhando
        if contagem_opcao1 > contagem_opcao2:
            frase = (
                        estado + "\nOpção 1 com mais votos. " + "Data: " + self.data1 + ", Horário: " + self.horario1 + " no local: " + self.local + "\nTotal de votos na opção 1: " + contagem_opcao1 + "\nTotal de votos na opção 2: " + contagem_opcao2 + "\nParticipantes que votaram: " + usuarios_ja_votaram)
            return frase
        elif contagem_opcao1 < contagem_opcao2:
            frase = (
                        estado + "\nOpção 2 com mais votos. " + "Data: " + self.data2 + ", Horário: " + self.horario2 + " no local: " + self.local + "\nTotal de votos na opção 1: " + contagem_opcao1 + "\nTotal de votos na opção 2: " + contagem_opcao2 + "\nParticipantes que votaram: " + usuarios_ja_votaram)
            return frase
        elif (contagem_opcao1 == 0) and (contagem_opcao2 == 0):
            frase = estado + "\nNenhum voto registrado."
            return frase
        else:
            frase = (
                    estado + "\nEmpate!" + "Total de votos na opção 1: " + contagem_opcao1 + ", total de votos na opção 2: " + contagem_opcao2 + contagem_opcao2 + "\nParticipantes que votaram: " + usuarios_ja_votaram)
            return frase

    def consultar_resultado(self):
        # Retorna o resultado final da enquete, disponibilizado quando ela é encerrada
        contagem_opcao1 = str(len(self.votosOpcao1))
        contagem_opcao2 = str(len(self.votosOpcao2))

        if contagem_opcao1 > contagem_opcao2:
            frase = ("A opção 1 foi escolhida pela maioria dos votantes. Local: " + self.local + ". Data: " + self.data1 + ". Horário: " + self.horario1)
        elif contagem_opcao2 > contagem_opcao1:
            frase = ("A opção 2 foi escolhida pela maioria dos votantes. Local: " + self.local + ". Data: " + self.data2 + ". Horário: " + self.horario2)
        elif contagem_opcao1 == '0' and contagem_opcao2 == '0':
            frase = "Nenhum usuário votou nesta enquete"
        elif contagem_opcao1 == contagem_opcao2:
            frase = "A votação resultou em empate."
        else:
            frase = "Os resultados ainda são inconclusivos"
        return frase

    def finalizar_enquete(self):
        # Finalizando a enquete
        self.enqueteAtiva = False
