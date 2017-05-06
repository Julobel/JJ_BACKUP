#!/usr/bin/python3
# -*-coding:utf-8 -*

import zipfile
import os
import tarfile

#constantes pour le type de compression
COMPRESS_NONE = "Aucun"
COMPRESS_ZIP = "zip"
COMPRESS_GZ = "gz"
COMPRESS_BZ2 = "bz2"
    
def compressFile(filePath,archiveType):
    """
    compresse un fichier dans une archive du même nom dans le même dossier avec le système de compression spécifié et supprimme le fichier
    renvoie vrai si la procédure a fini avec succes
            faux si le fichier n'existe pas
    une ValueError si le système de compression n'est pas géré
    """
    if (archiveType==COMPRESS_ZIP):
        if (_zipFile(filePath)):
            os.remove(filePath)
    elif (archiveType in (COMPRESS_GZ,COMPRESS_BZ2)):
        if (_tarFile(filePath,archiveType)):
            os.remove(filePath)
    elif archiveType not in getCompressTypeList():
        raise ValueError('Invalid compession system')
    
def _zipFile(filePath):
    """
    crée un fichier zip du même nom que le fichier specifié dans le même dossier
    renvoie vrai si la procédure a fini avec succes
            faux si le fichier n'existe pas
    """
    success=False
    if (os.path.exists(filePath)):
        zipf = zipfile.ZipFile(filePath+'.zip', 'w', zipfile.ZIP_DEFLATED)
        zipf.write(filePath)
        zipf.close()
        success=True
    return success

#
def _tarFile(filePath,archiveType):
    """
    crée un fichier tar du même nom que le fichier specifié dans le même dossier avec la compression specifiée
    renvoie vrai si la procédure a fini avec succes
            faux si le fichier n'existe pas
    """
    success=False
    if (os.path.exists(filePath)):        
        tarFile = tarfile.open(filePath+'.tar.'+archiveType, 'w:'+archiveType)
        tarFile.add(filePath)        
        tarFile.close()
        success=True
    return success

def getCompressTypeList():
    """
    Retourne la liste des types de compression supportés
    """
    res=[]
    res.append(COMPRESS_NONE)
    res.append(COMPRESS_BZ2)
    res.append(COMPRESS_GZ)
    res.append(COMPRESS_ZIP)
    return res
