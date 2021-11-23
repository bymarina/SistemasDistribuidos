import Pyro4
from Servidor import Servidor


def main():
    # Iniciar o Daemon
    daemon = Pyro4.Daemon()

    # Registramos a classe do servidor
    uri = daemon.register(Servidor)
    ns = Pyro4.locateNS()
    ns.register('AplicaçãoDoServidor', uri)
    print("Servidor disponível!")

    # Inicia o loop aguardando clientes
    daemon.requestLoop()


if __name__ == "__main__":
    main()
