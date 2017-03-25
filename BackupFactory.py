from MySQLBackup import *

""" Classe usine permettant de créer des objets de type IBackup """
class BackupFactory:


    """ Constantes représentant chaque SGBD supporté """
    SGBD_MYSQL = "MySQL"

    """
    Créer et retourne un objet de type implemettant IBackup en fonction des options spécifiées
    Lève une exception si le SGBD spécifié dans les options n'est pas supporté par l'application
    """
    def create (options):
        if options.SGBD == BackupFactory.SGBD_MYSQL:
            return MySQLBackup(options)
        raise Exception ("SGBD non supporté")

    """ Retourne la liste des SGBD supportés """
    def getSupportedSGBD(self):
        res = []
        res = res.append(BackupFactory.SGBD_MYSQL)
        return res