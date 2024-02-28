import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import json
from ..config import Settings

settings = Settings()


class CryptoService:
        def encrypt(self, raw):
                raw = pad(raw.encode(),16)
                cipher = AES.new(settings.CRYPTO_KEY.encode('utf-8'), AES.MODE_ECB)
                return base64.b64encode(cipher.encrypt(raw))

        def decrypt(self, enc):
                cipher = AES.new(settings.CRYPTO_KEY.encode('utf-8'), AES.MODE_ECB)
                decrypted = unpad(cipher.decrypt(base64.b64decode(enc)),16)
                return decrypted.decode("utf-8", "ignore")

        def decryptDict(self, enc):
                cipher = AES.new(settings.CRYPTO_KEY.encode('utf-8'), AES.MODE_ECB)
                decrypted = unpad(cipher.decrypt(base64.b64decode(enc)),16)
                return json.loads(decrypted.decode("utf-8", "ignore"))