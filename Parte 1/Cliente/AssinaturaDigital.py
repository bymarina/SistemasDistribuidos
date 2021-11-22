from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random


class AssinaturaDigital(object):
    def __init__(self):
        # Criando uma semente randômica para gerar o pac chave privada/pública
        semente_randomica = Random.new().read

        # Criando o par de chaves
        par_de_chaves = RSA.generate(2048, semente_randomica)
        self.chave_publica = par_de_chaves.public_key().export_key()  # export key deixa a chave em bytes
        chave_privada = par_de_chaves

        # Criando o assinante
        self.assinante = pkcs1_15.new(chave_privada)

        # Modificando chave de bytes para string
        self.chave_publica_str = self.chave_publica.decode()

    def chave_publica_string(self):
        return self.chave_publica_str

    def assinar_mensagem(self, mensagem):
        # Criando o hash da mensagem:
        mensagem_bytes = bytes(mensagem, 'utf-8')
        digest = SHA256.new()
        digest.update(mensagem_bytes)

        # Assinando a mensagem
        assinatura_digital = self.assinante.sign(digest)
        return assinatura_digital
