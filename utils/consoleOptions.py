#!/usr/bin/python3
# -*-coding:utf-8 -*

from utils.functions import askChoice,askBoolean,getInt
from utils.backupFactory import BackupFactory
from utils.compress import getCompressTypeList

def askSGBD():
    """
    Demande un nom d'SGBD
    :return: String
    """
    return BackupFactory.getSupportedSGBD()[askChoice("\nChoisissez un SGBD: ", BackupFactory.getSupportedSGBD())]

def askHost():
    """
    Demande un nom de domaine ou une adresse IP
    :return: String
    """
    return input("\nEntrez le nom de domaine ou l'adresse IP de votre serveur: ")

def askPort():
    """
    Demande un numéro de port et le retourne
    :return: int
    """
    return getInt("\nEntrez le numéro du port utilisé: ",1, 65535)

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
    return getCompressTypeList()[askChoice("\nChoisisez ou non un type de compression: ", getCompressTypeList())]
