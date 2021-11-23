from ClienteCallback import ClienteCallback
from AssinaturaDigital import AssinaturaDigital
from Menu import Menu
from Pyro4 import util
import sys
import Pyro4
import threading as t


def main():
    # Obtém a referência da aplicação do servidor no serviço de nomes
    ns = Pyro4.locateNS()
    uri = ns.lookup('AplicaçãoDoServidor')
    servidor = Pyro4.Proxy(uri)
    sys.excepthook = Pyro4.util.excepthook

    # Inicializar o Pyro daemon e registrar o objeto Pyro cliente nele
    daemon = Pyro4.core.Daemon()
    cliente = ClienteCallback()
    uri_cliente = daemon.register(cliente)
    nc = Pyro4.locateNS()
    nc.register('Cliente', uri_cliente)

    # Instanciar a Assinatura Digital
    assinatura_digital = AssinaturaDigital()
    chave_publica = assinatura_digital.chave_publica_str

    # Inicializar a thread do cliente
    thread_cliente = t.Thread(target=cliente.loop_thread, args=(daemon,))
    thread_cliente.daemon = True
    thread_cliente.start()

    # Cadastrar cliente no servidor
    print("Cadastro de novo usuário: ")
    nome = input("Digite seu nome: ").strip()
    servidor.cadastrar_usuario(uri_cliente, nome, chave_publica)

    while True:
        # Mostrar o menu
        Menu.mostrar_menu(servidor, assinatura_digital)


if __name__ == "__main__":
    main()
