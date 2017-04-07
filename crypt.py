from random import randrange

def generateEncryptionKey(length):
    """
    Genère une chaine de caractère aléatoire de la longueur spécifiée
    :param key: integer longueur de la clé de cryptage à générer
    :return: string une clé aleatoire
    """
    akey=""
    for i in range (0,length):
        codeAscii = randrange(255)
        akey = akey + chr(codeAscii)
    return akey


def encryption(message,key):
    """
    Applique un cryptage symetrique du message spécifié avec la clé specifié
    cf   https://fr.wikipedia.org/wiki/Cryptographie_symétrique#Petite_taxinomie_du_chiffrement_sym.C3.A9trique_classique
    :param message: string le message à crypter
    :param key: string la clé de cryptage
    :return: string le message crypté
    """
    if (len(key)==0):
        return message
    messageArray=list(message)        
    keyArray=list(key)
    messageArray.append('.')
    modulus=len(messageArray)%len(keyArray)
    #on rajoute des * pour completer le message
    for i in range(0,len(keyArray)-modulus):
        messageArray.append("*")
    #on découpe le tableau
    tempArr=[]
    for i in range(0,len(messageArray),len(keyArray)):
        tempArr.append(messageArray[i:i+len(keyArray)])
    oldSort=_sortKey(keyArray)
    tempArr = _transposeDoubleArray(tempArr)
    msg=""
    for i in range(0,len(oldSort)):
        msg+=''.join(tempArr[oldSort[i]])
    return msg

def _transposeDoubleArray(tab):
    """
    transpose un tableau de ligne en un tableau de colonne
    :param tab: un tableau
    :return: List le tableau transposé
    """
    res=[]
    rowLength=len(tab[0])
    for j in range (0,rowLength):
        col=[]
        for i in range(0,len(tab)):       
            col.append(tab[i][j])
        res.append(col)
    return res

#
def _sortKey(keyArr):
    """
    tri un tableau et retourne un tableau avec les index de l'ancien ordre
    :param keyArr: un tableau
    :return: integer List le tableau des anciens index trié
    """
    result=[]
    for i in range(0,len(keyArr)):
        result.append(i)
    for i in range(len(keyArr),1,-1):
        for j in range( 0 , i-1):
            if keyArr[j] > keyArr[j+1]:
                tempIndex=result[j]
                result[j] = result[j+1]
                result[j+1] = tempIndex
                temp = keyArr[j]
                keyArr[j] = keyArr[j+1]
                keyArr[j+1] = temp
    return result

def decryption(message,key):
    """
    Décrypte un message d'après la clé fournie
    :param message: string le message à décrypter
    :param key: string la clé de décryptage
    :return: string le message décrypté
    :throw ValueError n°53236 si la cle n'est pas adaptée au message (longueur du message mod longueur de la clé différent de 0
    """
    if (len(key)==0):
        return message
    if ( len(message)% len(key)!=0):
        raise ValueError(53236,'Invalid crypt Key')
    messageArray=list(message)
    keyArray=list(key) 
    quotient=len(messageArray)//len(keyArray)
    tempArr=[]
    for i in range(0,len(messageArray),quotient):
        tempArr.append(messageArray[i:i+quotient])    
    oldSort=_sortKey(keyArray)   
    unsorttempArr=[]    
    for i in range(0,len(tempArr)):
        unsorttempArr.append(tempArr[oldSort.index(i)])    
    tempArr = _transposeDoubleArray(unsorttempArr)
    msg=""
    for i in range(0,len(tempArr)):
        msg+=''.join(tempArr[i])
    cpt=len(msg)    
    while(msg[cpt-1:cpt]!="."):
        msg = msg[:cpt-1]
        cpt = cpt -1
    msg = msg[:cpt-1]
    return msg
   
if __name__=="__main__":
    un_message="ceci est un /*message*/."
    key="crypto"
    crypted= encryption(un_message,key)
    print("crypted:",crypted)
    decrypted=decryption(crypted,key)
    print("decrypted:",decrypted)
    print("origine  :",un_message) 
    try:
        decryption(crypted,"1234567")
    except ValueError as e:
        if (e.args[0]==53236):
            print("Clé incorecte")
        else:
            print("une autre erreur")
   