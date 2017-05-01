# coding=utf-8

from functions import askChoice
from backupOptions import BackupOption
from MySQLBackup import MySQLBackup

def mainMenu ():
    while askChoice("\n################# MENU PRINCIPAL #################\n", ["Sauvegarder une base de donnée", "Quitter\n"]) == 0:
        options = BackupOption()
        options.recoveryOptions()
        MySQLBackup(options).execute()

mainMenu()