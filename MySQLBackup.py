from IBackup import IBackup
from pathlib import Path
from functions import displayError
import pymysql
import os, time

class MySQLBackup(IBackup):
    """
    Classe permettant de gérer la sauvegarde à une base de donnée MySQL
    Contient un attribut de type BackupOption contenant les paramètres nécessaires (CF BackupOption)
    """

    def __init__(self, options):
        """ Constructeur qui initialise l'attribut options """
        self.options = options

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
                displayError("Acces refusé! Vous ne disposez pas des droits nécessaires d'accès à la base")
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

    # TODO A redéfinir
    def execute(self): # utiliser l'objet option pour récupérer les paramètres            
        """
        Exécute la sauvegarde en fonction des options
        Et créé un dossier si inexistant par BDD, ainsi qu'un fichier dump MySql pour chaque base de données
        """
        counter = 0
        while counter < len(DBList):

            # creation d'un dossier pour cette base s'il n'existe pas
            backupDbPath = "backups/" + DBList[counter]
            print("Création du dossier pour le backup")
            if not os.path.exists(backupDbPath):
                os.makedirs(backupDbPath)

            # chemin et nom du fichier sql
            backupFilePath = backupDbPath + "/" + DBList[counter] + "-" + time.strftime('%d%m%Y-%H%M%S') + ".sql"

            # creation de la commande mysqldump
            dumpcmd = "mysqldump -u " + DBUser
            if (DBPwd != ""):
                dumpcmd += " -p" + DBPwd
            dumpcmd += " " + DBList[counter] + " > " + backupFilePath
            print("dumpcmd -> " + dumpcmd)

            # execution de la commande et recuperation du statut
            output = os.system(dumpcmd)

            # si la commande a echoue suppresion du fichier precedemment créer
            if output == 0:
                print("Le backup de la base de donnée '" + DBList[
                    counter] + "'a été créé dans le dans le dossier " + backupFilePath)
            else:
                print("La base de donnée n'existe pas ...")
                delWrongDb(backupFilePath)
            counter += 1
        
