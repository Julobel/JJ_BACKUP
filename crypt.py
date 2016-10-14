from random import randrange

#applique un cryptage symetrique du message spécifié avec la clé specifié
#retourne la chaine de caractère cryptée
#lève une erreur si le deux paramètres n'on pas la même longueur
def symetricEncryption(message,key):
    if ( len(message)!= len(key)):
        raise ValueError('Invalid crypt Key')
    
    tmpMessage=message
    tmpKey=key
    cryptMessage =""
    while(len(tmpMessage)>0):
        messageCharAscii = ord(tmpMessage[:1])
        keyCharAscii = ord(tmpKey[:1])
        cryptMessage = cryptMessage +chr(messageCharAscii^keyCharAscii);
        tmpMessage=tmpMessage[1:]
        tmpKey=tmpKey[1:]
    return cryptMessage

#genère une chaine de caractère aléatoire de la longueure spécifiée
def generateSymetricEncryptionKey(length):
    if(length==0):
        raise ValueError('Invalid length Key')
    akey=""
    for i in range (0,length):
        codeAscii = randrange(255)
        akey = akey + chr(codeAscii)
    return akey


if __name__=="__main__":
    message="lisq"
    key=generateSymetricEncryptionKey(len(message))
    print("key :",key)
    
    crypt=symetricEncryption(message,key)
    print("crypt :",crypt)
    
    decrypt=symetricEncryption(crypt,key)
    print("decrypt :",decrypt)
    
    