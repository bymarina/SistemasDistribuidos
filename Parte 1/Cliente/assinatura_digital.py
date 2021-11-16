from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA   
from Crypto import Random
from base64 import b64encode, b64decode 

class assinaturaDigital (object):
    def __init__ (self):
        #Criando uma semente randômica para gerar o pac chave privada/pública
        semente_randomica = Random.new().read

        #Criando o par de chaves
        par_de_chaves = RSA.generate(2048, semente_randomica)
        self.chave_publica = par_de_chaves.public_key().export_key() #export key deixa a chave em bytes
        self.chave_privada = par_de_chaves
        self.assinante = pkcs1_15.new(self.chave_privada)
        
        #Preparando para enviar a chave pública para o servidor
        #chave_publica_bytes = b64encode(self.chave_publica)
        self.chave_publica_str = self.chave_publica.decode()
    
    def chavePublicaBytes(self):
        return self.chave_publica

    def chavePublicaString(self):
        return self.chave_publica_str
    
    def chavePublica(self):
        return self.chave_publica
    
    def chavePrivada(self):
        return self.chave_privada
    
    def hashMensagem(self, mensagem):
        mensagemHash = SHA256.new(mensagem.encode('utf-8')).digest()
        return mensagemHash

    def assinarMensagem(self, mensagem):
        AssinaturaDigital = self.assinante.sign(mensagem)
        return AssinaturaDigital    