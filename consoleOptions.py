# coding=utf-8

from functions import *
import BackupFactory
import backupOptions
from compress import getCompressTypeList


def askSGBD():
    """
    Demande un nom d'SGBD
    :return: String
    """
    return askChoice("\nChoisissez un SGBD: ", BackupFactory.BackupFactory().getSupportedSGBD())

def askHost():
    """
    Demande un nom de domaine ou une adresse IP
    :return: String
    """
    return input("\nEntrez le nom de domaine ou l'adresse IP de votre serveur: ")

def askUser():
    """
    Demande un nom d'utilisateur et le retourne
    :return: String
    """
    return input("\nEntrez votre nom d'utilisateur: ")

def askPwd():
    """
    Demande un mot de passe et le retourne
    :return: String
    """
    return input("\nEntrez votre mot de passe: ")

def askAllDbs():
    """
    Demande si le programme doit sauvegarder toutes les bases de données
    :return: Boolean
    """
    return askBoolean("\nVoulez-vous sauvegarder toutes les bases de données présentent sur le serveur?")

def askDbs():
    """
    Demande la liste de la/les base(s) de données à sauvegarder
    :return: String List
    """
    dbTab = []
    while True:
        db = input("\nAjoutez une base de donnée à sauvegarder (Laissez vide pour quitter) : ")
        if db == '':
            return dbTab
        else:
            dbTab.append(db)
            continue

def askCrypt():
    """
    Demande si le programme doit crypter le fichier de dump
    :return: Boolean
    """
    return askBoolean("Voulez vous crypter vos fichiers de sauvegardes?")

def askCompressType():
    """
    Demande si le programme doit compresser le fichier de dump, et si oui de quel type
    :return: String
    """
    return askChoice("\nChoisisez ou non un type de compression: ", getCompressTypeList())

if __name__=="__main__":

    options = backupOptions.BackupOption

    options.sgbd = askSGBD()
    options.host = askHost()
    options.user = askUser()
    options.pwd = askPwd()
    options.allDatabases = askAllDbs()
    options.databases = askDbs()
    options.compressType = askCompressType()
    options.crypt = askCrypt()
