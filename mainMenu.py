# coding=utf-8

from consoleOptions import askChoice
from backupOptions import BackupOption
from MySQLBackup import MySQLBackup


def mainMenu ():
    if askChoice("################# MENU PRINCIPAL #################\n", ["Sauvegarder une base de donnée", "Quitter\n"]) == 0:
        options = BackupOption()
        options.recoveryOptions()
        MySQLBackup(options).execute()

mainMenu()