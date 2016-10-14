# -*- coding: utf8 -*-

import zipfile
import os
import tarfile

#compresse un fichier dans une archive du même nom dans le même dossier avec le système de compression spécifié
#renvoie vrai si la procédure a fini avec succes
#        faux si le fichier n'existe pas
#        une ValueError si le système de compression n'est pas géré
def compressFile(filePath,archiveType):
    if (archiveType=="zip"):
        return _zipFile(filePath)
    elif (archiveType in ("gz","bz2")):
        return _tarFile(filePath,archiveType)
    else:
        raise ValueError('Invalid compession system')

#crée un fichier zip du même nom que le fichier specifié dans le même dossier
#renvoie vrai si la procédure a fini avec succes
#        faux si le fichier n'existe pas
def _zipFile(filePath):
    success=False
    if (os.path.exists(filePath)):
        zipf = zipfile.ZipFile(filePath+'.zip', 'w', zipfile.ZIP_DEFLATED)
        zipf.write(filePath)
        zipf.close()
        success=True
    return success

#crée un fichier tar du même nom que le fichier specifié dans le même dossier avec la compression specifiée
#renvoie vrai si la procédure a fini avec succes
#        faux si le fichier n'existe pas
def _tarFile(filePath,archiveType):
    success=False
    if (os.path.exists(filePath)):        
        tarFile = tarfile.open('t.txt.tar.'+archiveType, 'w:'+archiveType)
        tarFile.add(filePath)        
        tarFile.close()
        success=True
    return success





