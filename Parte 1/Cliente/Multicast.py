import socket
import struct
import time


class Multicast:
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

    def escutar_multicast(self):
        while True:
            mensagem = self.sock.recv(10240)
            if mensagem is None or mensagem == b'':
                time.sleep(1)
                continue

            mensagem_decodificada = mensagem.decode()
            print("\nAtenção!")
            verificar_mensagem_recebida = mensagem_decodificada[0]

            if verificar_mensagem_recebida == "1":
                titulo_enquete = mensagem_decodificada[24:]
                self.cliente.mostrar_conteudo_para_cliente("Por gentileza vote na nova enquete criada: " + titulo_enquete)
            else:
                titulo_enquete = mensagem_decodificada[23:]
                print("Enquete finalizada: " + titulo_enquete)

            time.sleep(1)

    def pegar_referencias_cliente(self, servidor, cliente, uri_cliente):
        self.cliente = cliente
        self.uri_cliente = uri_cliente
        self.servidor = servidor
