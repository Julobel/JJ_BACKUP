import time,os
import pymysql
from IBackup import IBackup
from crypt import encryptFile
from functions import displayError, displayInfo, initLog, deletePath
from compress import compressFile,COMPRESS_NONE

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
            initLog().info("Connexion au serveur : "+ self.options.host+":"+str(self.options.port))
            return pymysql.connect(host=self.options.host, port=self.options.port, user=self.options.user, password=self.options.pwd,
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
            return pymysql.connect(host=self.options.host, port=self.options.port, user=self.options.user, password=self.options.pwd,
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
        """ Retourne un objet BackupOption correpondant aux options"""
        return self.options
    
    def getDatabases(self):
        """ 
        Retourne un tableau de string contenant la liste des bdd.
        """
        res=[]
        connection = self.serverConnect()
        if connection != None:
            cursor = connection.cursor()
            cursor.execute('SHOW DATABASES')
            database = cursor.fetchone()
            connection.close()
            while database:
                res.append(database['Database'])
                database = cursor.fetchone()
        return res
        
    def backup(self, dbName):
        """ 
        Créer un fichier sql du dump de la base de  données spécifié
        :return: String le chemin relatif du fichier créé
        """
        # creation d'un dossier pour cette base s'il n'existe pas
        backupDbPath = "backups/" + self.options.host.replace(".", "_") + "_" + dbName
        if not os.path.exists(backupDbPath):
            initLog().info("Création du dossier pour le backup : "+backupDbPath)
            os.makedirs(backupDbPath)

        # chemin et nom du fichier sql
        backupFilePath = backupDbPath + "/" + dbName + "-" + time.strftime('%Y%m%d-%H%M%S') + ".sql"

        # creation de la commande mysqldump
        dumpcmd = "mysqldump -u " + self.options.user + " -P " + str(self.options.port)
        if (self.options.pwd != ""):
            dumpcmd += " -p" + self.options.pwd
        if (self.options.host != ""):
            dumpcmd += " -h " + self.options.host
        dumpcmd += " " + dbName + " > " + backupFilePath
        initLog().info("dumpcmd -> " + dumpcmd)

        # execution de la commande et recuperation du statut
        output = os.system(dumpcmd)

        if output == 0:
            displayInfo("Le backup de la base de donnée '" + dbName
                        + "'a été créé dans le dans le dossier " + backupFilePath)
        else:
            deletePath(backupFilePath)
            raise ValueError(54627,"Impossible d'effectuer le dump de MySQL")
        return backupFilePath

    def execute(self):
        """
        Exécute la sauvegarde en fonction des options
        Et créé un dossier si inexistant par BDD, ainsi qu'un fichier dump MySql pour chaque base de données
        """ 
        if self.serverConnect() != None:
            for database in self.options.databases:
                if self.dbConnect(database) != None:
                    nameFilePath = self.backup(database)
                    if (self.options.crypt==True):
                        encryptFile(nameFilePath,self.options.cryptKey)
                    if(self.options.compressType != COMPRESS_NONE):
                        compressFile(nameFilePath, self.options.compressType)
