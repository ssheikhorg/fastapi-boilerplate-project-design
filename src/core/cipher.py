import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

from src import settings as c


class AESCipher:
    def __init__(self):
        self.str_to_bytes = lambda x: x.encode()
        self.key = self.str_to_bytes(c.aes_key)
        self.iv = self.str_to_bytes(c.aes_iv)

    def encrypt(self, raw):
        ciphertext = pad(self.str_to_bytes(raw), AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(ciphertext)).decode()

    def decrypt(self, hashed):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return unpad(cipher.decrypt(base64.b64decode(hashed)), AES.block_size).decode()
