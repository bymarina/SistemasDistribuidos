from multicast import multicast
import Pyro4
from servidor import servidor

def main():
    #Iniciar o Daemon
    daemon = Pyro4.Daemon()
    
    #Registramos a classe do servidor
    uri = daemon.register(servidor)
    ns = Pyro4.locateNS()
    ns.register('AplicaçãoDoServidor', uri)
    print("Servidor disponível!")
    multicasting = multicast()

    #Inicia o loop aguardando clientes
    daemon.requestLoop()

if __name__ == "__main__":
    main()