# coding=utf-8
# Script pour créer un backup d'une base de donnée sur mysql

# Importation des librairies nécessaires au script
from tkinter.filedialog import *
from pathlib import Path
import time, os


# Fonctions
def multiBackup(userBDD, userPassBDD, pathBackup, nameBDD):
    dbFile = open(nameBDD, "r")
    length = len(dbFile.readlines())
    counter = 1
    dbfile = open(nameBDD, "r")
    while counter <= length:
        bdd = dbfile.readline()
        bdd = bdd[:-1]
        backup = pathBackup + "/" + bdd
        if not os.path.exists(backup):
            os.makedirs(backup)
        backup += "/" + time.strftime('%d%m%Y-%H%M%S') + ".sql"
        dumpcmd = "mysqldump -u " + userBDD + " -p" + userPassBDD + " " + bdd + " > " + backup
        output = os.system(dumpcmd)
        counter += 1
        if output == 0:
            print("Le backup de la base de donnée '" + bdd + "'a été créé dans le dans le dossier " + backup)
            time.sleep(1)
        else:
            print("La base de donnée n'existe pas ...")
            print("Suppression du fichier et du dossier concerant une BDD non existante.")
            deleteWrongDB(backup)
    dbfile.close()

def oneBackup(userBDD, userPassBDD, pathBackup, nameBDD):
    backup = pathBackup + "/" + nameBDD
    print("Création du dossier pour le backup")
    if not os.path.exists(backup):
        os.makedirs(backup)
    bdd = nameBDD
    dumpcmd = "mysqldump -u " + userBDD + " -p" + userPassBDD + " " + bdd + " > " + backup + "/" + time.strftime(
        '%d%m%Y-%H%M%S') + ".sql"
    print("dumpcmd -> " + dumpcmd)
    os.system(dumpcmd)
    print("Le backup de la base de donnée '" + bdd + "'a été créé dans le dans le dossier " + backup)

def deleteWrongDB(backup):
    file_path = Path(backup)
    file_path.unlink()
    for parent, _ in zip(file_path.parents, range(1)):
        # On remonte de 1 dossier dans l'arborescence du fichier supprimer
        # Si le dossier est vide on le supprime sinon on retourne une erreur
        try:
            parent.rmdir()
        except OSError:
            break


# Main
hoteBDD = "localhost"
userBDD = input("Veuillez saisir votre nom d'utilisateur: ")
userPassBDD = input("Veuillez saisir votre mot de passe: ")
multi = input("Si vous souhaitez procéder à un seul backup taper '0' sinon tapez '1': ")
multi = int(multi)
if multi == 0:
    nameBDD = input("Veuillez entrer le nom de la base donnée que vous souahitez sauvegarder: ")
    pathBackup = askdirectory(initialdir='.')
    oneBackup(userBDD, userPassBDD, pathBackup, nameBDD)
else:
    nameBDD = askopenfilename()
    pathBackup = askdirectory(initialdir='.')
    multiBackup(userBDD, userPassBDD, pathBackup, nameBDD)