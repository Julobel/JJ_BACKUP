class BackupOption(object):
    '''
    Classe contenant les différentes options nécessaires à la sauvegarde
    sgbd : une constante representant le sgbd
    host : une chaine de caractere representant l'adresse IP ou le nom de domaine
    user : une chaine de caractere representant le nom d'utilisateur de la BDD
    pwd : une chaine de caractere representant le mot de passe de l'utilisateur de la BDD
    databases : un tableau contenant la liste des noms des bases à sauvegarder 
    allDatabases : un booleen representant si l'utilisateur veut sauvegarder toutes les BDD
    compressType : une constante representant le type de compression 
    crypt : un booleen representant si l'utilisateur veut crypter les fichiers
    '''
    
    #constantes pour le sgbd
    SGBD_MYSQL = "MySQL"
    SGBD_ORACLE = "Oracle"
    SGBD_SQLSERVER = "SQL Server"
    SGBD_POSTGRE = "PostgreSQL"
    SGBD_SQLLITE = "SQLite"
    

    def __init__(self,sgbd="", host="localhost",user="",pwd="",databases=[],allDatabases=False,compressType="",crypt=False):
        '''
        initialisation des attributs
        '''
        self.sgbd = sgbd
        self.host = host
        self.user = user
        self.pwd = pwd
        self.databases = databases
        self.allDatabases = allDatabases
        self.compressType = compressType
        self.crypt = crypt
     
    def addDatabase(self, database):
        if database not in self.databases:
            self.databases.append(database)
     
    def removeDatabase(self, database):
        if database in self.databases:
            self.databases.remove(database)
    
    