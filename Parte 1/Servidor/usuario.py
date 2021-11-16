from base64 import b64decode

class usuario:
    def __init__(self, nome, uri_cliente, chave_publica):
        self.nome = nome
        self.uri_cliente = uri_cliente
        self.chave_publica = chave_publica
        #self.chave_publica = b64decode(chave_publica)

    def nome(self):
        return self.nome
    
    def uri_cliente(self):
        return self.uri_cliente

    def retorna_chave_publica(self):
        chave_publica_bytes = self.chave_publica.encode('utf-8')
        return chave_publica_bytes

#chave_publica = b64decode(chave_publica["data"])
