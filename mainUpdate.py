
from PIL import Image
import cv2

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from unittest.mock import sentinel
from numpy import nper
import numpy

'''
from unidecode import unidecode


def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))
'''



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
    wide, tall, channel = turkey.shape
    w2, t2, ch2 = stuffing.shape
    
    stuffing = cv2.resize(stuffing, (tall, wide) )
    stuffing = cv2.cvtColor(stuffing, cv2.COLOR_BGR2GRAY)
    cv2.imshow('altered file2',stuffing)
    cv2.imshow('file1', turkey)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    for x in range( 0, wide ):
        for y in range( 0, tall):
            bwVal = stuffing.item(x,y)
            #bluVal = turkey.item(x,y,0)
            #greVal = turkey.item(x,y,1)
            redVal = turkey.item(x,y,2) #opencv BGR
            
            if bwVal == 0:
                newRed = redVal & 254
            else:
                newRed = redVal | 1
            turkey.itemset((x, y,2), newRed)  
    #cv2.    
    cv2.imshow('merged images', turkey )
    cv2.imshow('original', cv2.imread(file1))
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('savedMerged.png', turkey )   
            
def separateImage(inFile):
    
            
    
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
        print("Sbohem -goodbye in czech")
        break
    elif choice =='5':
        file1 = 'Star-Wars-Darth-Vader-Wallpaper.png'
        file2= 'star-wars-yoda-spinoff-film.png'
        hideImage( file1, file2 )
    #inFile = 'Star-Wars-The-Force-Awakens-R2-D2.png'
    #hideFile = 'hiddenImage.png'
    elif choice =='6':
        print("Select your image: ")
        inFile = askopenfilename()
        print (inFile)
        root.withdraw()
        separateImage( inFile )
    


    
    

