from Crypto.Cipher import AES
import os, binascii
import base64


def encryption():
	
	message =input('Please enter your message: ')
	length = 16 - (len(message)%16)
	x = len(message)
	for x in range (length):
		message += " "
	
	key = input('Please enter your key: ')
	keyLength = 16 - (len(key)%16)
	x = len(key)
	for x in range(keyLength):
		key += " "
	print(key)
	
	obj = AES.new(key,AES.MODE_CBC,'This is an IV456')
	cipherTextBytes = obj.encrypt(message)
	cipherText = base64.b64encode(cipherTextBytes).decode('ascii')
	print("This is the encrypted message: ", cipherText)
	
	
	
def decryption():
	cipherText = input('Please enter your message: ')
	cipherTextBytes = base64.b64decode(cipherText)
	key = input('Please enter your key: ')
	keyLength = 16 - (len(key)%16)
	x = len(key)
	for x in range(keyLength):
		key += " "
	obj2 = AES.new(key,AES.MODE_CBC,'This is an IV456')
	plain_text = obj2.decrypt(cipherTextBytes)
	plain_text = plain_text.decode()
	print(plain_text)
	
	
encryption()
decryption()
