import socket


class multicast:
    def __init__(self):
        self.MCAST_GRP = '224.1.1.1'
        self.MCAST_PORT = 5007
        # regarding socket.IP_MULTICAST_TTL
        # ---------------------------------
        # for all packets sent, after two hops on the network the packet will not
        # be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
        self.MULTICAST_TTL = 2
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.MULTICAST_TTL)

    def notificar_nova_enquete(self, enquete):
        message = str.encode("1: Nova enquete criada: " + enquete.titulo)
        self.sock.sendto(message, (self.MCAST_GRP, self.MCAST_PORT))

    def notificar_enquete_finalizada(self, enquete):
        message = str.encode("2: Enquete finalizada: " + enquete.titulo + ". Resultado: " + enquete.consultar_resultado())
        self.sock.sendto(message, (self.MCAST_GRP, self.MCAST_PORT))
