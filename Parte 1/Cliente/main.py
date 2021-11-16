from cliente_callback import cliente_callback
from multicast import multicast
from assinatura_digital import assinaturaDigital

import sys
import Pyro4
import threading as t

def main():  
    #Obtem a referência da aplicação do servidor no serviço de nomes
    ns = Pyro4.locateNS()
    uri = ns.lookup('AplicaçãoDoServidor')
    servidor = Pyro4.Proxy(uri)
    sys.excepthook = Pyro4.util.excepthook
 
    #Inicializar o Pyro daemon e registrar o objeto Pyro cliente nele
    daemon = Pyro4.core.Daemon()
    cliente = cliente_callback()
    uri_cliente = daemon.register(cliente)
    nc = Pyro4.locateNS()
    nc.register('Cliente', uri_cliente)

    #Instanciando a Assinatura Digital
    assinatura = assinaturaDigital()

    #Instanciando o Multicast

    objetoMulticast = multicast()
    objetoMulticast.referenciaCliente(servidor, cliente, uri_cliente)

    #Inicializando as threads 
    thread_cliente = t.Thread(target=cliente.loopThread, args=(daemon, ))
    thread_cliente.daemon = True
    thread_cliente.start()   

    thread_multicast = t.Thread(target=objetoMulticast.escutarMulticast, args=())
    thread_multicast.daemon = True
    thread_multicast.start()

    #O cliente deve ser cadastrado ao iniciar a aplicação
    cliente.cadastrarUsuario(servidor, uri_cliente, assinatura)

    while True:
        print("Bem-vindo(a) ao serviço de enquetes, as seguintes opções estão disponíveis: ")
        print("1 - Cadastrar nova enquete")
        print("2 - Consultar enquetes disponíveis")
        print("3 - Votar em uma enquete")
        print("4 - Sair")

        selection = input ("Por favor selecione uma opção: ") 
        if selection =='1': 
            cliente.cadastrarEnquete(servidor, uri_cliente)
        elif selection == '2': 
            cliente.consultarEnquetes(servidor)
        elif selection == '3':
            cliente.votarEmEnquete(servidor, uri_cliente)
        elif selection =='4':
            break
        else: 
            print ("Opção desconhecida!") 

if __name__ == "__main__":
    main()