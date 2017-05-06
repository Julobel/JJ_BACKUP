#!/usr/bin/python3
# -*-coding:utf-8 -*

from crypt import *

# Fonctions

'''
Permet de crypter le contenu d'un fichier .txt
@Param string key, cle de cryptage
'''
def encryptFile(key):
    # On recupere toutes les donnes du fichier dans un tableau
    with open('toCrypt.txt') as file:
        toEncryptTab = [line.rstrip() for line in file]

    # On crypte les donnees et on les insere dans un tableau
    cryptTab = []
    for i in range(0, len(toEncryptTab)):
        encryptElt = encryption(toEncryptTab[i],key)
        cryptTab.append(encryptElt)

    # On ecrit les donnes cryptees du tableau dans un fichier .txt
    open('encryptVersion.txt', 'w')
    ecrireLigne = open('encryptVersion.txt', 'a')
    for i in range (0, len(cryptTab)):
        ecrireLigne.write(cryptTab[i] + "\n")

'''
Permet de decrypter un fichier .txt
@Param string key, cle de decryptage
'''
def decryptFile(key):
    # On recupere toutes les donnes cryptees du fichier dans un tableau
    with open('encryptVersion.txt') as file:
        toDecryptTab = [line.rstrip() for line in file]

    # On decrypte les donnees et on les insere dans un tableau
    decryptTab = []
    for i in range (0, len(toDecryptTab)):
        d = decryption(toDecryptTab[i], key)
        decryptTab.append(d)

    # On ecrit les donnes decryptees du tableau dans un fichier .txt
    open('decryptVersion.txt', 'w')
    writeLine = open('decryptVersion.txt', 'a')
    for i in range (0, len(decryptTab)):
        writeLine.write(decryptTab[i] + "\n")

if __name__=="__main__":
    key = 'string'
    encryptFile(key)
    decryptFile(key)