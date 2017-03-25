from abc import ABC, abstractmethod

"""
Interface qui va définir les méthodes pour les futurs SGBD supportés
"""
class IBackup(ABC):

    """ Exécute la sauvegarde """
    @abstractmethod
    def execute(self):
        pass

    """ Se connecte au serveur """
    @abstractmethod
    def serverConnect(self):
        pass

    """ # Se connecte à la base de donnée spécifiée """
    @abstractmethod
    def DBConnect(self, DbName):
        pass

    """ Retourne un objet de type backupOption contenant les différents paramètres nécessaire à la sauvegarde """
    @abstractmethod
    def getOptions(self):
        pass

if __name__=="__main__":
    pass