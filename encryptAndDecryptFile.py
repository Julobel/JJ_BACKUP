from crypt import *

def encryptFile(key):
    with open('toCrypt.txt') as file:
        toEncryptTab = [line.rstrip() for line in file]

    cryptTab = []
    for i in range(0, len(toEncryptTab)):
        encryptElt = encryption(toEncryptTab[i],key)
        cryptTab.append(encryptElt)

    open('encryptVersion.txt', 'w')
    ecrireLigne = open('encryptVersion.txt', 'a')
    for i in range (0, len(cryptTab)):
        ecrireLigne.write(cryptTab[i] + "\n")

def decryptFile(key):
    with open('encryptVersion.txt') as file:
        toDecryptTab = [line.rstrip() for line in file]

    decryptTab = []
    for i in range (0, len(toDecryptTab)):
        d = decryption(toDecryptTab[i], key)
        decryptTab.append(d)

    open('decryptVersion.txt', 'w')
    writeLine = open('decryptVersion.txt', 'a')
    for i in range (0, len(decryptTab)):
        writeLine.write(decryptTab[i] + "\n")

if __name__=="__main__":
    key = 'string'
    encryptFile(key)
    decryptFile(key)