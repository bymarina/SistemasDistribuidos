class GerenciadorDeEnquetes:
    @staticmethod
    def tente_finalizar_enquete(objeto_enquete, objeto_multicast, lista_usuarios_cadastro):
        if not objeto_enquete:
            print("Enquete não localizada")
            return

        if GerenciadorDeEnquetes.todos_os_usuarios_votaram(objeto_enquete, lista_usuarios_cadastro):
            GerenciadorDeEnquetes.finaliza_enquete(objeto_enquete, objeto_multicast)
            return
        print("Ainda restam usuários para votar")

    @staticmethod
    def finaliza_enquete(objeto_enquete, objeto_multicast):
        objeto_enquete.finalizar_enquete_por_votos()
        objeto_multicast.notificar_enquete_finalizada(objeto_enquete)
        objeto_enquete.consultar_andamento_enquete()

    @staticmethod
    def todos_os_usuarios_votaram(objeto_enquete, lista_usuarios_cadastro):
        for pessoa in lista_usuarios_cadastro:
            if not GerenciadorDeEnquetes.checar_se_usuario_votou(objeto_enquete, pessoa):
                return False
        return True

    @staticmethod
    def checar_se_usuario_votou(enquete, pessoa):
        usuario_votou = enquete.checar_se_usuario_votou(pessoa.nome)
        if not usuario_votou:
            return False
        return True
