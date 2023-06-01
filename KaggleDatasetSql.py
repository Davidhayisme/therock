from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import numpy as np
import os
import pymysql
from faker import Faker

def AddToDB(RFS):
    nameFake = Faker()
    serverIP = "127.0.0.1"
    databaseUserName = "john"
    databasePassword = "ChrisKringle$7"
    charSet = "utf8mb4"
    cursorType = pymysql.cursors.DictCursor
    connectMYSQL = pymysql.connect(host=serverIP,user=databaseUserName,password=databasePassword,charset=charSet,cursorclass=cursorType)
    theCursor = connectMYSQL.cursor()
    try:
        theCursor.execute("CREATE DATABASE "+RFS[0])
    except:
        print("Database already created, following files will be added")
    engine = create_engine("mysql+pymysql://{}:{}@{}:3306/{}".format(databaseUserName,databasePassword,serverIP,RFS[0]), echo=False)
    engine.connect()
    originalPath = RFS[1]+"/"
    fileCheck = RecursiveFileCheck(originalPath,engine)
    if fileCheck != False:
        RealFunction(originalPath,engine,nameFake)
        print("Done")

def RealFunction(path,engine,nameFake):
    filelist = os.listdir(path)
    for i in filelist:
        if i.__contains__("."):
            df1 = pd.read_csv(path+i, delimiter=',', nrows=None)
            df1.to_sql(nameFake.first_name().lower(), engine, index=False)
        else:
            RecursiveFileCheck(originalPath + i + "/", engine)

def RecursiveFileCheck(path,engine):
    filelist = os.listdir(path)
    for i in filelist:
        if i.__contains__("."):
            try:
                df1 = pd.read_csv(path+i, delimiter=',', nrows=None)
                #df1.to_sql(nameFake.first_name, engine, index=False)
            except:
                print("There weren't valid file types to store")


        else:
            RecursiveFileCheck(originalPath + "/" + i, engine)