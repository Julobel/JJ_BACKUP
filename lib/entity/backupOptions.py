#!/usr/bin/python3
# -*-coding:utf-8 -*

import configparser
from lib.view.consoleOptions import askSGBD,askHost,askUser,askPwd,askAllDbs,askDbs,askCrypt,askCompressType,askPort
from lib.utils.functions import stringToBoolean
from lib.entity.backupFactory import BackupFactory

class BackupOption():
    """
    Classe contenant les différentes options nécessaires à la sauvegarde
    sgbd : une constante representant le sgbd
    host : une chaine de caractere representant l'adresse IP ou le nom de domaine
    port : un entier representant le numero du port utilisé par le protocole
    user : une chaine de caractere representant le nom d'utilisateur de la BDD
    pwd : une chaine de caractere representant le mot de passe de l'utilisateur de la BDD
    databases : un tableau contenant la liste des noms des bases à sauvegarder 
    allDatabases : un booleen representant si l'utilisateur veut sauvegarder toutes les BDD
    compressType : une constante representant le type de compression 
    crypt : un booleen representant si l'utilisateur veut crypter les fichiers
    cryptKey : une chaine de caractere representant la clé de cryptage
    """

    def __init__(self,sgbd="",host="localhost",port=3306,user="root",pwd="root",databases=[], allDatabases=False,compressType="",crypt=False,cryptKey=""):
        """
        initialisation des attributs
        """
        self.sgbd = sgbd
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.databases = databases
        self.allDatabases = allDatabases
        self.compressType = compressType
        self.crypt = crypt
        self.cryptKey = cryptKey

    def recoveryOptions(self):
        """ hydrate les attributs par saisie au terminal """
        self.sgbd = askSGBD()
        self.host = askHost()
        self.port = askPort()
        self.user = askUser()
        self.pwd = askPwd()
        self.allDatabases = askAllDbs()
        if not self.allDatabases:
            print('\n'.join(BackupFactory.create(self).getDatabases()))
            self.databases = askDbs()
        self.crypt = askCrypt()
        if self.crypt:
            self.cryptKey = input("Entrez une clé de cryptage: ")
        self.compressType = askCompressType()

    def addDatabase(self, database):
        """ ajoute une bdd à la liste """
        if database not in self.databases:
            self.databases.append(database)

    def removeDatabase(self, database):
        """ supprimme une bdd de la liste """
        if database in self.databases:
            self.databases.remove(database)

    def __str__(self, *args, **kwargs):
        """ couvertit l'objet en chaine de caractères """
        res = {'sgbd': self.sgbd,
                                'host': self.host,
                                'port': self.port,
                                'user': self.user,
                                'pwd': self.pwd,
                                'databases':self.databases,
                                'allDatabases': self.allDatabases,
                                'compressType': self.compressType,
                                'crypt': self.crypt,
                                'cryptKey': self.cryptKey
                                }
        return res.__str__()

    def saveToConfFile(self,filePath):
        """ sauvegarde les option dans un fichier conf dans le fichier spécifié"""
        config = configparser.ConfigParser()
        config['options'] =  {'sgbd': self.sgbd,
                                'host': self.host,
                                'port': self.port,
                                'user': self.user,
                                'pwd': self.pwd,
                                'allDatabases': self.allDatabases,
                                'compressType': self.compressType,
                                'crypt': self.crypt,
                                'cryptKey': self.cryptKey
                                }

        config['options']['databases'] =','.join(self.databases)
        with open(filePath, 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def createFromConfFile(filePath):
        """ Retourne un objet BackupOption à partir du fichier conf spécifié """
        config = configparser.ConfigParser()
        config.read(filePath)
        option = BackupOption()
        option.sgbd = config['options']['sgbd']
        option.host = config['options']['host']
        option.port = int(config['options']['port'])
        option.user = config['options']['user']
        option.pwd = config['options']['pwd']
        if(len(config['options']['databases'])==0):
            option.databases = []
        else:
            option.databases = config['options']['databases'].split(",")
        option.allDatabases = stringToBoolean(config['options']['allDatabases'])
        option.compressType = config['options']['compressType']
        option.crypt = stringToBoolean(config['options']['crypt'])
        option.cryptKey = config['options']['cryptKey']
        return option
