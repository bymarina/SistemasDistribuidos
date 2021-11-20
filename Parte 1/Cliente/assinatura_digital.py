from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA   
from Crypto import Random
import base64

class assinaturaDigital (object):
    def __init__ (self):
        #Criando uma semente randômica para gerar o pac chave privada/pública
        semente_randomica = Random.new().read

        #Criando o par de chaves
        par_de_chaves = RSA.generate(2048, semente_randomica)
        self.chave_publica = par_de_chaves.public_key().export_key() #export key deixa a chave em bytes
        chave_privada = par_de_chaves

        #Criando o assinante
        self.assinante = pkcs1_15.new(chave_privada)
        
        #Modificando chave de bytes para string
        self.chave_publica_str = self.chave_publica.decode()
    
    def chavePublicaBytes(self):
        return self.chave_publica

    def chavePublicaString(self):
        return self.chave_publica_str

    def assinarMensagem(self, mensagem):
        #Criando o hash da mensagem:
        mensagemBytes = bytes(mensagem, 'utf-8')
        digest = SHA256.new()
        digest.update(mensagemBytes)
        #Assinando a mensagem
        AssinaturaDigital = self.assinante.sign(digest)
        return AssinaturaDigital    