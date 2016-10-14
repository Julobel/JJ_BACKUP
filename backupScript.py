# coding=utf-8
# Script pour créer un backup d'une base de donnée sur mysql

# Importation des librairies nécessaires au script
from tkinter.filedialog import *
from pathlib import Path
import time, os


# Fonctions
#creation d'un fichier sql d'une base de données
def oneBackup(userBDD, userPassBDD, nameBDD):
	#creation d'un dossier pour cette base s'il n'existe pas
    backupBDDPath =  "backups/" + nameBDD
    print("Création du dossier pour le backup")
    if not os.path.exists(backupBDDPath):
        os.makedirs(backupBDDPath)
	#chemin et nom du fichier sql
    backupFilePath = backupBDDPath + "/" + nameBDD + "-" + time.strftime('%d%m%Y-%H%M%S') + ".sql"
	
	#creation de la commande mysqldump
    dumpcmd = "mysqldump -u " + userBDD 
    if(userPassBDD!=""):
        dumpcmd += " -p" + userPassBDD
    dumpcmd += " " + nameBDD + " > " + backupFilePath
    print("dumpcmd -> " + dumpcmd)
    print("Le backup de la base de donnée '" + nameBDD + "'a été créé dans le dans le dossier " + backupBDDPath)
	
	#execution de la commande et recuperation du statut
    output = os.system(dumpcmd)
	#si la commande a echoue suppresion du fichier precedemment créer
    if output == 0:
        print("Le backup de la base de donnée '" + nameBDD + "'a été créé dans le dans le dossier " + backupFilePath)
        time.sleep(1)
    else:
        print("La base de donnée n'existe pas ...")
        print("Suppression du fichier et du dossier concerant une BDD non existante.")
        deleteWrongDB(backupFilePath)
    
#creation d'un fichier sql pour plusieurs base de données 
def multiBackup(userBDD, userPassBDD, nameBDDList):
	#recuperation du fichier contenant la liste des base de données à sauvegarder
    dbFile = open(nameBDDList, "r")
    nbBDD = len(dbFile.readlines())
    counter = 1
    dbfile = open(nameBDDList, "r")
	
	#pour chaque ligne du fichier, appel à la methode de sauvegarde d'une base
    while counter <= nbBDD:
		#lecture de la ligne et suppression du saut de ligne
        nameBDD = dbfile.readline()
        if(counter!=nbBDD):
            nameBDD = nameBDD[:-1]
        oneBackup(userBDD,userPassBDD,nameBDD)
        counter += 1
    dbfile.close()

#suppresion d'un fichier et de son dossier parent s'il est vide
def deleteWrongDB(backupFilePath):
    #suppression du fichier
    file_path = Path(backupFilePath)
    file_path.unlink()
    #suppression du dossier parent, s'il est vide
    for parent, _ in zip(file_path.parents, range(1)):
        # On remonte de 1 dossier dans l'arborescence du fichier supprimer
        # Si le dossier est vide on le supprime sinon on retourne une erreur
        try:
            parent.rmdir()
        except OSError:
			print (OSError)
            break

#creation d'un fichier avec les bases de données et retourne son chemin
def writeListDb():	
    name = 'dbListAuto.txt'
    dbFile = open(name, "w")
    restart = True
    counter = 1
    while restart:
        if counter == 1:
            dbFile.write(input("Entrez une bdd à backup: "))
        else:
            dbFile.write("\n" + input("Entrez une bdd à backup: "))
        counter += 1
        res = input("Voulez ajouter une bdd ? (oui/non): ")
        if res == "oui":
            restart = True
        else:
            dbFile.close()
            restart = False
    print("Le fichier " + name + "bien été créé")
    return name
	
#creation d'un fichier avec les bases de données
def writeListDb():	

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
    nameBDD = writeListDb()
    pathBackup = askdirectory(initialdir='.')
    multiBackup(userBDD, userPassBDD, pathBackup, nameBDD)