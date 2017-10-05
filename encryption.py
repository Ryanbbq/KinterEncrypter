from Crypto.Cipher import AES
import os, binascii

<<<<<<< HEAD

=======
rand_string2 = os.urandom(16)
rand_string = binascii.b2a_hex(os.urandom(16))

message =input('Please enter your message: ')
length = 16 - (len(message)%16)
x = len(message)
for x in range (length):
	message += " "
	
	
obj = AES.new(rand_string,AES.MODE_CBC,rand_string2)
ciphertext = obj.encrypt(message)
print("This is the encrypted message: ", ciphertext)
#print(rand_string)
#asciiKey = str(rand_string,'utf-8')
asciiKey = rand_string.decode()
print ("This is the message ",asciiKey)
>>>>>>> c54ac703e0f167d4b378e75ebc851413549bf6ea

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
	ciphertext = obj.encrypt(message)
	print("This is the encrypted message: ", ciphertext)
	
	
	return ciphertext

<<<<<<< HEAD
def decryption(cipher):
	ciphertext = input('Please enter your message: ')
	
	key = input('Please enter your key: ')
	keyLength = 16 - (len(key)%16)
	x = len(key)
	for x in range(keyLength):
		key += " "
	print(key)
	obj2 = AES.new(key,AES.MODE_CBC,'This is an IV456')
	plain_text = obj2.decrypt(cipher)
	plain_text = plain_text.decode()
	print(plain_text)
	
	
cipher = encryption()

decryption(cipher);
=======
obj2 = AES.new(asciiKey,AES.MODE_CBC,rand_string2)
plain_text = obj2.decrypt(ciphertext)
plain_text = plain_text.decode()
print(plain_text)
>>>>>>> c54ac703e0f167d4b378e75ebc851413549bf6ea
