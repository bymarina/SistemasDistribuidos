from Notificar import Notificar


class GerenciadorDeEnquetes:
    @staticmethod
    def tente_finalizar_enquete(objeto_enquete, lista_usuarios_cadastro):
        if not objeto_enquete:
            print("Enquete não localizada")
            return

        if GerenciadorDeEnquetes.verificar_se_todos_os_usuarios_votaram(objeto_enquete, lista_usuarios_cadastro):
            GerenciadorDeEnquetes.finalizar_enquete(objeto_enquete, lista_usuarios_cadastro)
            return

    @staticmethod
    def finalizar_enquete(objeto_enquete, lista_usuarios_cadastro):
        objeto_enquete.finalizar_enquete()
        lista_clientes_a_serem_notificados = GerenciadorDeEnquetes.pegar_referencia_votantes(lista_usuarios_cadastro, objeto_enquete.retornar_todos_os_votantes())
        notificacao = ("\nA seguinte enquete foi finalizada: " + objeto_enquete.titulo + "\n" + objeto_enquete.consultar_resultado())
        Notificar.notificar_clientes(notificacao, lista_clientes_a_serem_notificados)

    @staticmethod
    def verificar_se_todos_os_usuarios_votaram(objeto_enquete, lista_usuarios_cadastro):
        for pessoa in lista_usuarios_cadastro:
            if not GerenciadorDeEnquetes.checar_se_um_usuario_votou(objeto_enquete, pessoa):
                return False
        return True

    @staticmethod
    def checar_se_um_usuario_votou(enquete, pessoa):
        usuario_votou = enquete.checar_se_usuario_votou(pessoa.nome)
        if not usuario_votou:
            return False
        return True

    @staticmethod
    def pegar_referencia_votantes(lista_usuarios_cadastro, lista_votantes):
        lista_notificar_final_enquete = []
        for votante in lista_votantes:
            for usuario in lista_usuarios_cadastro:
                if usuario.nome == votante:
                    lista_notificar_final_enquete.append(usuario)
        return lista_notificar_final_enquete
