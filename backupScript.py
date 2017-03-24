# coding=utf-8
# Script pour créer un backup d'une base de donnée sur mysql

from pathlib import Path
import os, time

# Fonctions
'''
Création d'un tableau contenant le ou les noms des BDDs
@Param boolean multi, false si l'utilisateur souhaite fait un backup pour une seule base sinon vaut vrai
@Return array listDb, contient le ou les noms des bases de données à backup
'''
def tabListDb(multi):
    listDb = []
    if multi == 0:
        listDb.append(input("Entrez le nom de la BDD à backup: "))
    else:
        restart = True
        while restart:
            listDb.append(input("Entrez le nom de la BDD à backup: "))
            res = input("Voulez ajouter une bdd ? (y/n): ")
            if res == "y":
                restart = True
            else:
                restart = False
    print("Les BDD que vous souhaitez backup sont -> " + str(listDb))
    return listDb

'''
Création d'un fichier backup .sql pour la ou les bases de données
@Param string userDB, nom d'utilisateur de la base de donnée
@Param string userPassDb, mot de passe utilisateur de la bas e de donnée
@Param array listDb, contient le ou les noms des bases de données à backup
'''
def backup(userDb, userPassDb, listDb):
    counter = 0
    while counter < len(listDb):
        # creation d'un dossier pour cette base s'il n'existe pas
        backupDbPath =  "backups/" + listDb[counter]
        print("Création du dossier pour le backup")
        if not os.path.exists(backupDbPath):
            os.makedirs(backupDbPath)
        # chemin et nom du fichier sql
        backupFilePath = backupDbPath + "/" + listDb[counter] + "-" + time.strftime('%d%m%Y-%H%M%S') + ".sql"

        # creation de la commande mysqldump
        dumpcmd = "mysqldump -u " + userDb
        if(userPassDb != ""):
            dumpcmd += " -p" + userPassDb
        dumpcmd += " " + listDb[counter] + " > " + backupFilePath
        print("dumpcmd -> " + dumpcmd)

        # execution de la commande et recuperation du statut
        output = os.system(dumpcmd)

        # si la commande a echoue suppresion du fichier precedemment créer
        if output == 0:
            print("Le backup de la base de donnée '" + listDb[counter] + "'a été créé dans le dans le dossier " + backupFilePath)
        else:
            print("La base de donnée n'existe pas ...")
            delWrongDb(backupFilePath)
        counter += 1
'''
Supprime le fichier et le dossier créé si la procédure ne c'est pas passé comme prévu (Ex: erreur dans le nom de la bdd ..)
@Param string backupFilePath, chemin du fichier à supprimer
'''
def delWrongDb(backupFilePath):
    # suppression du fichier
    file_path = Path(backupFilePath)
    file_path.unlink()
    # suppression du dossier parent, s'il est vide
    for parent, _ in zip(file_path.parents, range(1)):
        # On remonte de 1 dossier dans l'arborescence du fichier supprimer
        # Si le dossier est vide on le supprime sinon on retourne une erreur
        try:
            parent.rmdir()
        except OSError:
            print (OSError)
            break

if __name__=="__main__":
    hoteBDD = "localhost"
    userDb = input("Veuillez saisir votre nom d'utilisateur: ")
    userPassDb = input("Veuillez saisir votre mot de passe: ")
    multi = input("Si vous souhaitez procéder à un seul backup taper '0' sinon tapez '1': ")
    multi = int(multi)
    listDb = tabListDb(multi)
    backup(userDb, userPassDb, listDb)
