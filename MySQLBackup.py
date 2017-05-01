from IBackup import IBackup
from pathlib import Path

from backupOptions import BackupOption
from functions import displayError, displayInfo
import pymysql
import time
import sys, os

class MySQLBackup(IBackup):
    """
    Classe permettant de gérer la sauvegarde à une base de donnée MySQL
    Contient un attribut de Mytype BackupOption contenant les paramètres nécessaires (CF BackupOption)
    """

    def __init__(self, options):
        """ Constructeur qui initialise l'attribut options """
        self.options = options # type: BackupOption

    def serverConnect(self):
        """
        Retourne une connexion au SGBD
        si une erreur se produit, affiche le message et renvoie None
        """
        try:
            return pymysql.connect(host=self.options.host, user=self.options.user, password=self.options.pwd,
                charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        except pymysql.err.OperationalError as e1:
            if(e1.args[0]==2003):
                displayError("Impossible de se connecter au serveur")
            elif(e1.args[0]==1045):
                displayError("Acces refusé! Vous ne disposez pas des droits nécessaires d'accès au serveur ")
            else:   
                displayError("Error " +str(e1.args[0])+"\n"+e1.args[1])
            return None
        
    def dbConnect(self, dbName):     
        """
        Retourne une connexion à la bdd spécifiée du SGBD en option
        si une erreur se produit, affiche le message et renvoie None
        """   
        try:
            return pymysql.connect(host=self.options.host, user=self.options.user, password=self.options.pwd,
                 db=dbName,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        except pymysql.err.OperationalError as e1:
            if(e1.args[0]==1044):
                displayError("Accès refusé! Vous ne disposez pas des droits nécessaires d'accès à la base")
            else:   
                displayError("Error " +str(e1.args[0])+"\n"+e1.args[1])        
        except pymysql.err.InternalError as e2:
            if(e2.args[0]==1049):
                displayError("La base de données n'éxiste pas")
            else:   
                displayError("Error " +str(e2.args[0])+"\n"+e2.args[1])
        except Exception as e3:
            #pour le debugage et retour utilisateur
            displayError("Error " +str(e3.args[0])+"\n"+e3.args[1])
        return None   

    def getOptions(self):
        return self.options
    
    def getDatabases(self):
        """ 
        Retourne un tableau de string contenant la liste des bdd. 
        Retourne None si une erreur de connexion se produit
        """
        try:
            res=[]
            connection = self.serverConnect()
            cursor = connection.cursor()
            cursor.execute('SHOW DATABASES')
            database = cursor.fetchone()
            connection.close()
            while database:
                res.append(database['Database'])
                database = cursor.fetchone()
            return res
        except Exception as e:
            return None

    def backup(self, dbName):
        # creation d'un dossier pour cette base s'il n'existe pas
        backupDbPath = "backups/" + dbName + self.options.host.replace(".", "_")
        print("Création du dossier pour le backup")
        if not os.path.exists(backupDbPath):
            os.makedirs(backupDbPath)

        # chemin et nom du fichier sql
        backupFilePath = backupDbPath + "/" + dbName + "-" + time.strftime('%Y%m%d-%H%M%S') + ".sql"

        # creation de la commande mysqldump
        dumpcmd = "mysqldump -u " + self.options.user
        if (self.options.pwd != ""):
            dumpcmd += " -p" + self.options.pwd
        if (self.options.host != ""):
            dumpcmd += " -h " + self.options.host
        dumpcmd += " " + dbName + " > " + backupFilePath
        print("dumpcmd -> " + dumpcmd)

        # execution de la commande et recuperation du statut
        output = os.system(dumpcmd)

        if output == 0:
            displayInfo("Le backup de la base de donnée '" + dbName
                        + "'a été créé dans le dans le dossier " + backupFilePath)
        return backupFilePath

    def execute(self):
        """
        Exécute la sauvegarde en fonction des options
        Et créé un dossier si inexistant par BDD, ainsi qu'un fichier dump MySql pour chaque base de données
        """
        if self.serverConnect() != None:
            for counter in range(0, len(self.options.databases)):
                if self.dbConnect(self.options.databases[counter]) != None:
                    nameFilePath = self.backup(self.options.databases[counter])

if __name__=="__main__":
    # if os.isatty(sys.stdin.fileno()):
    option = BackupOption()
    option.recoveryOptions()
    MySQLBackup(option).execute()
    # else:
    #     print("En graphique")
    #pip install cx_freeze
