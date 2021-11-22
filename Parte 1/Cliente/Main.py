from ClienteCallback import ClienteCallback
from Multicast import Multicast
from AssinaturaDigital import AssinaturaDigital

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

    # Instanciando a Assinatura Digital
    assinatura = AssinaturaDigital()
    cliente.referenciar_assinatura_digital(assinatura)

    # Instanciando o Multicast
    objeto_multicast = Multicast()
    objeto_multicast.pegar_referencias_cliente(servidor, cliente, uri_cliente)

    # Inicializando a thread do cliente
    thread_cliente = t.Thread(target=cliente.loop_thread, args=(daemon,))
    thread_cliente.daemon = True
    thread_cliente.start()

    # Inicializando a thread do multicast
    thread_multicast = t.Thread(target=objeto_multicast.escutar_multicast, args=())
    thread_multicast.daemon = True
    thread_multicast.start()

    # O cliente deve ser cadastrado ao iniciar a aplicação
    cliente.cadastrar_usuario(servidor, uri_cliente)

    while True:
        # Solicita o menu do servidor
        print(servidor.menu(uri_cliente))


if __name__ == "__main__":
    main()
