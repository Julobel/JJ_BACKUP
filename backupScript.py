# coding=utf-8
# Script pour créer un backup d'une base de donnée sur mysql

# Importation des librairies nécesaires au script
import os
import time

# Initialisaton des informations pour accéder à la BDD
hoteBDD = "localhost"
userBDD = "root"
userPassBDD = "root"
# nameBDD = "backups/namesBDD.txt                                              # Pour backup multiples
nameBDD = "backupTest"
cheminBackup = "./backups/"

# Utilisation de datetime pour créer le fichier de sauvegarde
dateBackup = time.strftime('%d%m%Y-%H%M%S')

backup = cheminBackup + dateBackup

# Vérification de l'existence du dossier de sauvegarde, si non, on le créé
print ("Création du dossier pour le backup")
if os.path.exists(backup):
    os.makedirs(backup)

# Condition si plusieurs backups ou non
if os.path.exists(nameBDD):
    file1 = open(nameBDD)
    multi = 1
    print ("Fichier de la base de donnée localisée")
    print ("Démarrage du backup de la base de donnée " + nameBDD)
else:
    print ("Fichier de la pas de donnée non localisée")
    print ("Démarrage du backup de la base de donnée " + nameBDD)
    multi = 0

# Procédure pour le backup
if multi == 1:
    fichier = open(nameBDD, "r")
    longueur = len(fichier.readlines())
    fichier.close()
    compteur = 1
    dbfile = open(nameBDD,"r")

    while compteur <= longueur:
        bdd = dbfile.readline()         # Lecture de la base de donnée depuis le fichier
        bdd = bdd[:-1]                  # Supprime les lignes supplémentaires
        dumpcmd = "mysqldump -u " + userBDD + " -p" + userPassBDD + " " + bdd + " > " + backup + "/" + bdd + ".sql"
        os.system(dumpcmd)
        compteur = compteur + 1
    dbfile.close()
else:
    bdd = nameBDD
    dumpcmd = "mysqldump -u " + userBDD + " -p" + userPassBDD + " " + bdd + " > " + backup + "/" + bdd + ".sql"
    os.system(dumpcmd)

print ("Backup terminé")
print ("Le backup a été créé dans le " + backup + " fichier")