import socket
import struct
import time

class multicast():
    def __init__(self):
        MCAST_GRP = '224.1.1.1'
        MCAST_PORT = 5007
        IS_ALL_GROUPS = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if IS_ALL_GROUPS:
            # on this port, receives ALL multicast groups
            self.sock.bind(('', MCAST_PORT))
        else:
            # on this port, listen ONLY to MCAST_GRP
            self.sock.bind((MCAST_GRP, MCAST_PORT))
        mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    def escutarMulticast(self):
        while True:
            mensagem = self.sock.recv(10240)
            print(mensagem)
            mensagemDecodificada = mensagem.decode()
            verificarMensagemRecebida = mensagemDecodificada[0]

            if verificarMensagemRecebida == "1":                
                tituloEnquete = mensagemDecodificada [24:]
                self.cliente.votarEmEnquete(self.servidor, self.uri_cliente, tituloEnquete)

            else:
                tituloEnquete = mensagemDecodificada [23:]
                print("Enquete finalizada: " + tituloEnquete)

            time.sleep(1)            

    def referenciaCliente(self, servidor, cliente, uri_cliente):
        self.cliente = cliente
        self.uri_cliente = uri_cliente
        self.servidor = servidor