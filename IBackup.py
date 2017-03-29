from abc import ABC, abstractmethod

class IBackup(ABC):
    """
    Interface qui va définir les méthodes pour les futurs SGBD supportés
    """

    @abstractmethod
    def execute(self):
        """ Exécute la sauvegarde """
        pass

    @abstractmethod
    def serverConnect(self):
        """ Se connecte au serveur et retourne la connexion"""
        pass

    @abstractmethod
    def dbConnect(self, dbName):      
        """ Se connecte à la base de donnée spécifiée et retourne la connexion"""
        pass

    @abstractmethod
    def getOptions(self):    
        """ Retourne un objet de type BackupOption contenant les différents paramètres nécessaire à la sauvegarde """
        pass

    @abstractmethod
    def getDatabases(self):    
        """ Retourne la liste des bases de données présentes sur le serveur """
        pass
    
if __name__=="__main__":
    pass