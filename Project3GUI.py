from tkinter import *
from tkinter.ttk import *
from tkinter import Tk
from PIL import Image
from tkinter.filedialog import askopenfilename
from unittest.mock import sentinel
from Crypto.Cipher import AES
import numpy as np
import cv2
import os

ciphertext=''

class App():
  def __init__(self, master):
    frame = Frame(master)
    frame.pack()
  
    master.title("Security Team")
    self.labelEncrypt = Label(frame, text="Encrypt")
    self.labelDecrypt= Label(frame,text="Decrypt")
    self.entryDecrypt=Entry(frame)
    self.entryEncrypt = Entry(frame)
    self.keyLabel = Label(frame,text="Key")
    self.keyEntry=Entry(frame)
    self.encryptEntry = Button(frame,text="Encrypt",width=15,command=self.encryptMessage)
    self.button = Button(frame,text="Quit", width=15,command=frame.quit)
    self.buttonCV= Button(frame,text="Turn on Camera",width=15,command=self.openCam)
    self.decryptEntry = Button(frame,text="Decrypt", width=15,command=self.decryptMessage)
    self.ImageHider = Button(frame,text="Image Hider",width=15,command=self.imageHider)
    #entry boxes
    self.entryDecrypt.grid(row=2,column=1)
    self.keyEntry.grid(row=1,column=1)
    self.entryEncrypt.grid(row=0, column=1)
    #labels
    self.labelDecrypt.grid(row=2,column=0)
    self.labelEncrypt.grid(row=0, column=0)
    self.keyLabel.grid(row=1,column=0)
    self.decryptEntry.grid(row=3, column=1,sticky='e')
    self.button.grid(row=8, column=1,sticky='e')
    self.buttonCV.grid(row=8,column=0,sticky='e')
    self.encryptEntry.grid(row=3,column=0,sticky='e')
    self.ImageHider.grid(row=5,column=1,sticky='e')

  
  def imageHider(self):
    def LSB( pixVal, bit ):
        if bit == '1':
            pixVal = pixVal | 1 #00000001
        else:
            pixVal = pixVal & 254 #11111110
        return pixVal


    def getLSB( pixVal ):
        if pixVal & 1 == 0:
            return '0' 
        else:
            return '1'

    def hide(inFile, secretMess):
        secretMess = secretMess + chr(0) #It will be the end of secretMessage marker
        
        hiddenPixList = []
                
        img = Image.open( inFile )
        img = img.convert('RGBA')  #four values per pixel
            
        pixList = list( img.getdata() )
            
        for i in range( len( secretMess ) ):
            asciiChar = ord( secretMess[i] )
            #print(asciiChar)
            binaryChar = bin( asciiChar ) [2:] .zfill( 8 )
            #print( binaryChar)    
            #Two separate lists keep the bits from alternating if they were stored in one list.
            hidePixEven = [] #contains bits 0-3
            hidePixOdd = []  #contains bits 4-7
                
            pixEven = pixList[ i*2 ]    # two pixels per binary number
            pixOdd = pixList[ (i*2) +1 ]  
                
            for k in range( 0, 4 ):
                hidePixEven.append( LSB( pixEven[k], binaryChar[k] ) )
                #print( hidePixEven)
                hidePixOdd.append( LSB( pixOdd[k], binaryChar[ k+4 ] ) )    
                #print(hidePixOdd)
            hpeTuple = tuple( hidePixEven )
            #print(hpeTuple)
            hpoTuple = tuple( hidePixOdd )
            #print(hpoTuple)  
            hiddenPixList.append( hpeTuple )
            hiddenPixList.append( hpoTuple )
            #print(hiddenPixList)
        unusedImgPart = pixList[ len(secretMess) *2: ]  #Splice n Dice the original image list
        hiddenPixList.extend( unusedImgPart )
        
        #for i in range(0,10):
            #print(hiddenPixList[i])
        
        newImg = Image.new( img.mode,img.size )
        newImg.putdata( hiddenPixList )
        newImg.save('hiddenImage.png')
        
        print("Success.")       


    def seek(hideFile):
        pixList=[]
        hiddenImg = Image.open(hideFile)
        hiddenImg = hiddenImg.convert('RGBA')
        pixList = list( hiddenImg.getdata() )
        #print(len(pixList))
        
        #for i in range( 100, 110):
        #print( pixList)
            
        messBinary ='0b'   
        decodeMess = ""
        bitCount = 0
        i=0
        
        while (messBinary != '0b00000000'):
            if bitCount == 8:
                decodeMess += chr(int(messBinary,2))
                messBinary = '0b'
                bitCount = 0
            
            tupleVal = pixList[i]
            #print("tupleval")
            #print( tupleVal )
            for item in tupleVal:
                #print("item")
                #print( item )
                messBinary += getLSB(item)
                #print("getLSB")
                #print( getLSB(item))
                bitCount += 1
                #print("bitcount")
                #print(bitCount)
            i+= 1
            #print("i")
            #print( i)
            #wtf = input("pause")
        print("Your secret message: ")
        print( decodeMess )

    def hideImage( file1, file2):
        turkey = cv2.imread(file1)
        stuffing = cv2.imread(file2)
        width, height, channel = turkey.shape
        stuffing = cv2.resize(stuffing, (width,height) )
        bwStuff = cv2.cvtColor(stuffing, cv2.COLOR_BGR2GRAY)
        cv2.imshow('bw',bwStuff)
        
        
        
    #This is a check to see if the correct image is being processed.
    def seeBoth( inFile, hideFile ):
        imBefore = cv2.imread(inFile)
        imAfter = cv2.imread(hideFile)
        cv2.imshow('Before', imBefore)
        cv2.imshow('After', imAfter)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    #main
    root = Tk()

    while( True ):
        print("Steganography")
        print("1. Encrypt Text")
        print("2. Decrypt Text")
        print("3. Compare before & after")
        print("4. Exit")
        choice = input("Enter your poison: ")
        if choice == '1':
            #http://stackoverflow.com/questions/11664443/raw-input-across-multiple-lines-in-python
            print("Enter your secret mess")
            #sentinel = 'team48'
            #secretMess = ''
            #for line in iter(input, sentinel): 
            secretMess=''+ '\n'.join(iter(input, 'team48' ))
            
            #secretMess = input("Enter you secret mess: ")
            print("Select your image: ")
            inFile = askopenfilename()
            print (inFile)
            root.withdraw()
            hide( inFile, secretMess )
        elif choice == '2':
            print("Select your image: ")
            hideFile = askopenfilename()
            #root.withdraw()
            seek( hideFile )
        elif choice == '3':
            seeBoth( inFile, hideFile )
        elif choice == '4':
            print("Sbohem -czech")
            break
        elif choice =='5':
            file1 = 'Star-Wars-Darth-Vader-Wallpaper.png'
            file2= 'star-wars-yoda-spinoff-film.png'
            hideImage( file1, file2 )
        #inFile = 'Star-Wars-The-Force-Awakens-R2-D2.png'
        #hideFile = 'hiddenImage.png'


  def decryptMessage(self):
    message=self.entry.get()
    key1=self.entry2.get()
    obj2 = AES.new(key1,AES.MODE_CFB,'This is an IV456')
    global ciphertext
    decryptedMessage=obj2.decrypt(ciphertext)
    print("This is the decrypted message: ",decryptedMessage)

  def openCam(self):
    cap=cv2.VideoCapture(0)
    fist_cascade = cv2.CascadeClassifier('C:\\Users\\Ryan\\Desktop\\Project3-master\\fist.xml')
    while(True):
      ret,frame=cap.read()
      gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
      fist=fist_cascade.detectMultiScale(gray,1.3,5)

      for(x,y,w,h) in fist:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,150,0),2)
      
      cv2.imshow('Fist',frame)
      if cv2.waitKey(1)&0xFF==ord('q'):
        break

    cap.release()

    cv2.destroyAllWindows()


  def encryptMessage(self):
    rand_string = os.urandom(16)
    message =input('Please enter your message: ')
    length = 16 - (len(message)%16)
    x = len(message)
    for x in range (length):
      message += " "
    obj = AES.new(rand_string,AES.MODE_CBC,'This is an IV456')
    ciphertext = obj.encrypt(message)
    print("This is the encrypted message: ", ciphertext)

    

root = Tk()
root.style = Style()

#('clam', 'alt', 'default', 'classic')
root.style.theme_use("clam")
#root.geometry("500x500")

app = App(root)
root.mainloop()
