import random
import numpy as np
import pandas as pd
import kaggle
from faker import Faker
from cryptography.fernet import Fernet
from datetime import datetime
import KaggleDatasetSql as kg
import Changes
import requests
import subprocess
import os
from http import HTTPStatus
import zipfile
'''
Usage: 
5/29/23 10:14 AM - David Hay
Adding worst-case testing, else statements, edge cases
'''
#add input parameter
def ChangingCol(df1):
    while(True):
        #Use a dictionary with numbers as a key to make this better l8r
        typeList = ["encryption","replacement","scrambling","shuffling","static Masking","tokenization"]
        typing = input("""What type of protection would you like to do:
Encryption, Replacement, Scrambling, Shuffling,
Static Masking, or Tokenization? Type done to end \n""")
        typing = typing.lower()
        #Checking if it contains the user input
        if typeList.__contains__(typing):
            col = input("What is the column name you would like?\n")
            #Checking if the column is present within the dataset
            if df1.keys().__contains__(col):
                #Gets and drops the dataframe column the user input
                tempCol = df1[col]
                df1.drop([col], axis=1)
                #Checks through all the methods
                if typing == typeList[0]:
                    #Calls methods in the changes file
                    df1[col] = Changes.EncryptionColumn(tempCol)
                    #Unique date and format to store different files with no overflow
                    CurrentTime = datetime.now()
                    df1.to_excel(col + "-" + "Encryption" + "-" + CurrentTime.strftime("%H-%M-%S")+ ".xlsx")
                elif typing == typeList[1]:
                    df1[col] = Changes.ReplacementColumn(tempCol)
                    CurrentTime = datetime.now()
                    df1.to_excel(col + "-" + "Replacement" + "-" + CurrentTime.strftime("%H-%M-%S") + ".xlsx")
                elif typing == typeList[2]:
                    df1[col] = Changes.ScramblingColumn(tempCol)
                    CurrentTime = datetime.now()
                    df1.to_excel(col + "-" + "Scrambling" + "-" + CurrentTime.strftime("%H-%M-%S") + ".xlsx")
                elif typing == typeList[3]:
                    df1[col] = Changes.ShufflingColumn(tempCol)
                    CurrentTime = datetime.now()
                    df1.to_excel(col + "-" + "Shuffling" + "-" + CurrentTime.strftime("%H-%M-%S") + ".xlsx")
                elif typing == typeList[4]:
                    df1[col] = Changes.StaticMaskingColumn(tempCol)
                    CurrentTime = datetime.now()
                    df1.to_excel(col + "-" + "Static_Masking" + "-" + CurrentTime.strftime("%H-%M-%S") + ".xlsx")
                elif typing == typeList[5]:
                    df1[col] = Changes.TokenizationColumn(tempCol)
                    CurrentTime = datetime.now()
                    df1.to_excel(col + "-" + "Tokenization" + "-" + CurrentTime.strftime("%H-%M-%S") + ".xlsx")
                else:
                    print("Not a valid column")
        elif typing.lower() == "done":
            return df1
        else:
            print("Unfortunately that was not an option.")
"""
Date        updated by      Comment
5/30/23     David Hay       Dynamic Synthetic Data added
5/31/23     Akram           update log
"""
def CreateSyntheticData(type, col):
    fake = Faker()
    newCol = []
    #Tries to eval function and if it doesn't exist it returns false
    try:
        for h in col:
            #Used to allow for any of the faker typing
            newCol.append(eval(str("fake." + type + "()")))
        return newCol
    except:
        return False
def SyntheticDataColumn(col):
    while(True):
        dataType = input("""What kind of data would you like to put into the columns?
If you would to see the data options, write help
If you want to leave, please write done. """)
        if dataType.lower() == "done":
            return col
        elif dataType.lower() == "help":
            fakeHelp = Faker()
            h = dir(fakeHelp)
            for x in h:
                print(x)
            continue
        newCol = CreateSyntheticData(dataType.lower(), col)
        if newCol != False:
            return newCol
        else:
            print("Not a valid synthetic data type")
#Changelog: Who changed what when
"""
5/30/23
David Hay
Calls the synthetic data function and prints it into an excel file
"""
def FakeDataCall(df1):
    while (True):
        columnName = input(f"Please input the exact name of the column you want to add or say done \n")
        if columnName != "done":
            #If column exists it does this
            if df1.keys().__contains__(columnName):
                #Drops the column so it can be readded with the same name
                tempCol = df1[columnName]
                df1.drop([columnName], axis=1)
                #Goes to get the synthetic data and store it
                df1[columnName] = SyntheticDataColumn(tempCol)
                #Unique file name
                CurrentTime = datetime.now()
                df1.to_excel(columnName + "-" + "Synthetic Data" + "-" + CurrentTime.strftime("%H-%M-%S") + ".xlsx")
            else:
                print("Not a valid column name")
        else:
            return df1
"""
5/31/23
David Hay
Added to put less pressure on the main method
"""
def DataframeExcelFile():
    while(True):
        #Checks if the file exists
        FileName = input("Please give the file you want to work with: \n")
        if os.path.exists(FileName):
            return FileName
        else:
            print("Not a valid file name")
def KaggleDatasetFinding():
    userInput = input("What keyword would you like to use?")
    k = subprocess.getoutput("kaggle datasets list -s " + userInput)
    h = k.split("\n", 2)
    # print(h[2])
    c = h[2].split("\n", 5)
    r = c[:5]
    try:
        for i in range(5):
            print(r[i])
    except:
        print("There were a limited amount of results")
    DatasetLoading(c)
def DatasetLoading(c):
    while (True):
        datasetChoice = input("""Which dataset would you like? Choose by number. 
If you want 5 more, just type more.
If you would like to change, type back \n""")
        if(datasetChoice) == "back":
            KaggleDatasetFinding()
            break
        try:
            choice = c[int(datasetChoice) - 1]
            finalSplit = choice.split(" ", 1)
            subprocess.run("kaggle datasets download -d " + finalSplit[0])
            RFS = finalSplit[0].split("/")
            if os.path.exists(RFS[1]):
                print("This dataset has already been loaded")
            else:
                with zipfile.ZipFile(RFS[1] + ".zip", "r") as theZip:
                    theZip.extractall(RFS[1])
            os.remove(RFS[1] + ".zip")
            kg.AddToDB(RFS)
            KaggleDatasetFinding()
        except:
            print("Not a valid input or a number or too high")
        break
    KaggleDatasetFinding()
def main():
    option = input("Would you like to do it yourself?")
    if option.lower() == "yes":
        while(True):
            filename = DataframeExcelFile()
            #Tries to see if reading the file into a dataframe is successful
            #if not it catches the error and restarts the method
            try:
                df1 = pd.read_csv(filename, delimiter=',', nrows = None)
                print("Success")
                break
            except:
                print("Not a valid file type")
                continue
        #Calling the rest of the functions
        df1.name = filename
        df1 = FakeDataCall(df1)
        df1 = ChangingCol(df1)
        kg.AddToDB(df1)
    else:
        KaggleDatasetFinding()

main()