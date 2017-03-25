from IBackup import IBackup
from pathlib import Path
import os, time

"""
Classe permettant de gérer la sauvegarde à une base de donnée MySQL
Contient un attribut de type BackupOption contenant les paramètres nécessaires (CF BackupOption)
"""
class MySQLBackup(IBackup):

    """ Constructeur qui initialise l'attribut options """
    def __init__(self, options):
        self.options = options

    # TODO à développer
    def serverConnect(self):
        pass

    # TODO à développer
    def DBConnect(self, DbName):
        pass

    def getOptions(self):
        return self.options

    '''
    Exécute la sauvegarde en fonction des options
    Et créé un dossier si inexistant par BDD, ainsi qu'un fichier dump MySql pour chaque base de données
    '''

    # TODO A redéfinir
    def execute(self): # utiliser l'objet option pour récupérer les paramètres
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

