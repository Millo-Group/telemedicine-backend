import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import json

key = 'a9abc2503dd038a0' 


class CryptoService:
        def encrypt(self, raw):
                raw = pad(raw.encode(),16)
                cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
                return base64.b64encode(cipher.encrypt(raw))

        def decrypt(self, enc):
                cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
                decrypted = unpad(cipher.decrypt(base64.b64decode(enc)),16)
                return decrypted.decode("utf-8", "ignore")

        def decryptDict(self, enc):
                cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
                decrypted = unpad(cipher.decrypt(base64.b64decode(enc)),16)
                return json.loads(decrypted.decode("utf-8", "ignore"))