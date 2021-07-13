import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES

import os

class AESCipher():

	def __init__(self, key):

		self.bs = AES.block_size
		self.key = base64.b64decode(key)


	def encrypt(self, raw):

		raw = self.pad(raw)
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return base64.b64encode(iv + cipher.encrypt(raw.encode()))

	def decrypt(self, enc):

		enc = base64.b64decode(enc)
		iv = enc[:16]
		cipher = AES.new(self.key, AES.MODE_CBC, iv)

		plaintext = str(cipher.decrypt(enc[16:]).decode())
		return plaintext

	def pad(self, s):

		return s + (self.bs - len(s) % self.bs) * "\x00"


	def unpad(self,s):

		return s[:-ord(s[len(s)-1:])]

def key_generator():

	key = base64.b64encode(os.urandom(32)).decode()
	return key

def EncryptString(text,key):

	func = AESCipher(key)
	res = func.encrypt(text).decode()
	return res


def DecryptString(enc_text,key):

	func = AESCipher(key)
	decoded = func.decrypt(enc_text)
	print (decoded)
	return (decoded)



