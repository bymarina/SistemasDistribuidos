class Menu:
    @staticmethod
    def mostrar_menu(servidor, assinatura_digital):
        menu = (
                    "\nBem vindo(a) ao serviço de enquetes, as seguintes opções estão disponíveis: " + "\n 1: Cadastrar nova enquete" + "\n 2: Consultar enquete" + "\n 3: Votar em enquete")
        print(menu)
        selecao = input("Selecionar: ").strip()
        Menu.opcao(selecao, servidor, assinatura_digital)

    @staticmethod
    def opcao(selecao, servidor, assinatura_digital):
        if selecao == '1':
            print("\nCadastro de nova enquete: ")
            nome = input("Digite seu nome: ").strip()
            titulo = input("Título da enquete: ").strip()
            local = input("Local: ").strip()
            data1 = input("Opção 1 de data: ").strip()
            horario1 = input("Horário: ").strip()
            data2 = input("Opção 2 de data: ").strip()
            horario2 = input("Horario: ").strip()
            limite = input("Data limite da enquete (formato: AAAA-MM-DD): ").strip()
            resultado = servidor.cadastrar_enquete(nome, titulo, local, data1, horario1, data2, horario2, limite)
            print(resultado)

        elif selecao == '2':
            nome = input("Digite seu nome: ").strip()
            titulo = input("Título da enquete: ").strip()
            mensagem = "Desejo consultar esta enquete"
            assinatura = assinatura_digital.assinar_mensagem(mensagem)
            resultado = servidor.consultar_enquete(nome, titulo, mensagem, assinatura)
            print(resultado)

        elif selecao == '3':
            nome = input("Digite seu nome: ").strip()
            titulo = input("Título da enquete: ").strip()
            informativo = servidor.solicitar_informativo_para_votacao(titulo)
            if informativo != "\nEsta enquete já foi finalizada":
                print(informativo)
                voto = input("Digite 1 para selecionar a data/horario 1 ou 2 para selecionar a data/horario 2: ").strip()
                resultado = servidor.votar(nome, titulo, voto)
                print(resultado)
            else:
                print(informativo)

        elif selecao != '' and selecao is not None:
            print("\nOpção de menu inválida")
