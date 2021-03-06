from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import base64


class AssinaturaDigital(object):
    @staticmethod
    def verificar_assinatura(mensagem, assinatura, objeto_usuario):
        chave_publica = objeto_usuario.retorna_chave_publica()
        chave_publica_rsa = RSA.importKey(chave_publica)
        assinante_chave_publica = pkcs1_15.new(chave_publica_rsa)
        if objeto_usuario is None:
            return "Erro na localização do usuário"
        else:
            # Transformando a mensagem em hash
            mensagem_bytes = bytes(mensagem, 'utf-8')
            digest = SHA256.new()
            digest.update(mensagem_bytes)
            try:
                # decodificando assinatura e realizando a verificação
                assinatura_decodificada = base64.b64decode(assinatura["data"])
                assinante_chave_publica.verify(digest, assinatura_decodificada)
                return True
            except (ValueError, TypeError):
                print("Assinatura inválida")
                return False
