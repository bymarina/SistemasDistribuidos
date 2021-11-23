class GerenciadorDeEnquetes:
    @staticmethod
    def tente_finalizar_enquete(objeto_enquete, lista_usuarios_cadastro, gerenciador_de_mensagens):
        # Realiza uma tentativa de finalizar a enquete

        # Verificando se a enquete existe
        if not objeto_enquete:
            print("Enquete não localizada")
            return

        # Verificando se todos os usuário votaram
        if GerenciadorDeEnquetes.verificar_se_todos_os_usuarios_votaram(objeto_enquete, lista_usuarios_cadastro):
            # Solicitando fechamento da enquete por votos
            GerenciadorDeEnquetes.finalizar_enquete(objeto_enquete, gerenciador_de_mensagens)
            return

    @staticmethod
    def verificar_se_todos_os_usuarios_votaram(objeto_enquete, lista_usuarios_cadastro):
        # Verificando se todos os usuários cadastrados no servidor votaram na enquete
        for pessoa in lista_usuarios_cadastro:
            if not GerenciadorDeEnquetes.checar_se_um_usuario_votou(objeto_enquete, pessoa):
                return False
        return True

    @staticmethod
    def checar_se_um_usuario_votou(enquete, pessoa):
        # Verificando se um usuário específico já votou na enquete
        usuario_votou = enquete.checar_se_usuario_votou(pessoa.nome)
        if not usuario_votou:
            return False
        return True

    @staticmethod
    def finalizar_enquete(objeto_enquete, gerenciador_de_mensagens):
        # Solicitando encerramento da enquete
        objeto_enquete.finalizar_enquete()
        # Solicitando notificações de encerramento de enquete
        gerenciador_de_mensagens.notificar_criador_enquete_finalizada()
        gerenciador_de_mensagens.notificar_votantes_enquete_finalizada()


