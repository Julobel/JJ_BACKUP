#!/usr/bin/python3
# -*-coding:utf-8 -*

from lib.entity.mySQLBackup import MySQLBackup

class BackupFactory:
    """ Classe usine permettant de créer des objets de type IBackup """
        
    """ Constantes représentant chaque SGBD supporté """
    SGBD_MYSQL = "MySQL"
    

    @staticmethod
    def create(options):
        """
        Créer et retourne un objet de type implemettant IBackup en fonction des options spécifiées
        Lève une exception si le SGBD spécifié dans les options n'est pas supporté par l'application
        """
        if options.sgbd == BackupFactory.SGBD_MYSQL:
            return MySQLBackup(options)
        raise Exception (53238,"SGBD non supporté")
   
    @staticmethod
    def getSupportedSGBD():
        """ Retourne la liste des SGBD supportés """ 
        res = []
        res.append(BackupFactory.SGBD_MYSQL)
        return res