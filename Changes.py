import random
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet
"""
5/30/23
David Hay
Generating a file to keep the encryption key seperate
for decryption
"""
def EncryptionColumn(col):
    #Generating the key into a file
    CurrentTime = datetime.now()
    key = Fernet.generate_key()
    with open(CurrentTime.strftime("%H-%M-%S") + ".key", "wb") as theKey:
        theKey.write(key)

    #Using the key to encrypt the rows in the column
    encrypter = Fernet(key)
    newCol = []
    for x in col:
        newCol.append(encrypter.encrypt(x.encode()))
    return newCol
"""
5/30/23
David Hay
Creating the code to choose between numbers and letters
"""
def ReplacementColumn(col):
    while(True):
        numLet = input("Numbers, Letters, or both \n")
        newCol = []
        if(numLet.lower() == "numbers"):
            # Chooses a random lowercase letter for replacing
            for x in col:
                tempString = ""
                for h in x:
                    tempString += chr(random.randint(65,89))
                newCol.append(tempString)
            return newCol
        elif(numLet.lower() == "letters"):
            # Chooses a random number
            for x in col:
                tempString = ""
                for h in x:
                    tempString += chr(random.randint(48,57))
                newCol.append(tempString)
            return newCol
        elif(numLet.lower() == "both"):
            for x in col:
                #Chooses between both with another random number
                tempString = ""
                for h in x:
                    alpha = random.randint(65,89)
                    num = random.randint(48,57)
                    if(random.randint(0,1) == 1):
                        tempString += chr(num)
                    else:
                        tempString += chr(alpha)
                newCol.append(tempString)
            #print(newCol)
            return newCol
        elif numLet.lower() == "done":
            return col
        else:
            print("Please input one of the given options or write done for no change")
"""
5/30/23
David Hay
Swapping characters in column and returning it
"""
def ScramblingColumn(col):
    newCol = []
    for x in col:
        strList = list(x)
        for h in range(len(strList)):
            tempRand = random.randint(0,len(strList)-1)
            #Uses a temp variable to swap the two values
            tempChar = strList[h]
            strList[h] = strList[tempRand]
            strList[tempRand] = tempChar
        newCol.append(''.join(strList))
    return newCol
"""
5/30/23
David Hay
Swap places of rows in column
"""
def ShufflingColumn(col):
    rcol = list(col)
    for x in range(len(rcol)):
        #Uses temp variable to store the row and swaps them
        tempRand = random.randint(0,len(col)-1)
        tempCol = rcol[x]
        rcol[x] = rcol[tempRand]
        rcol[tempRand] = tempCol
    return rcol
"""
5/30/23
David Hay
Choosing the symbol that does the masking
"""
def StaticMaskingColumn(col):
    newCol = []
    while(True):
        #Gets a symbol
        maskingSymbol = input("What symbol would you like to mask with?\n")
        if len(maskingSymbol) == 1:
            for x in col:
                strList = list(x)
                for h in range(len(strList)):
                    #Replaces anything with the symbol
                    strList[h] = maskingSymbol
                newCol.append(''.join(strList))
            return newCol
        else:
            print("Please input just one symbol")
"""
5/30/23
David Hay
Quickly gives a token to each respective row
"""
def TokenizationColumn(col):
    #Renames everything to T#
    newCol = []
    for x in range(len(col)):
        newCol.append("T"+str(x))
    return newCol


