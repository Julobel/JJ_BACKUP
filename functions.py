# coding=utf-8
from tkinter import messagebox
import logging
import sys

def centerFrame(frame):
    """ fonction permettant de centrer une fenêtre sur l'écran """
    frame.withdraw()
    frame.update_idletasks()
    x = (frame.winfo_screenwidth() - frame.winfo_reqwidth()) / 2
    y = (frame.winfo_screenheight() - frame.winfo_reqheight()) / 2
    frame.geometry("+%d+%d" % (x, y))
    frame.deiconify()

def display(message,title=""):
    """ affiche un message dans une pop up ou en console suivant les ressources du système """     
    if(sys.stdout.isatty()):
        if (title!=""): print("\n----"+title+"----")
        print(message)
        if (title!=""): print("\n-------------------")
    else:
        messagebox.showinfo(title, message)

def displayInfo(message):
    """ affiche un message dans une pop up ou en console suivant les ressources du système et enregistre le message dans les logs """    
    display(message,"Information")
    initLog().info(message)

def displayError(message):
    """ affiche une erreur dans une pop up ou en console suivant les ressources du système et enregistre le message dans les logs """
    if(sys.stdout.isatty()):
        print("----Erreur----")
        print(message)
    else:
        messagebox.showerror("Erreur", message)
    initLog().error(message)
    
    
def initLog():
    """ 
    initialise les paramètres de logging : 
    fichier backup.log en mode append et UTF8
    format : date - level : message
    :return: Logger objet
    """    
    logger= logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('backup.log', 'a', 'utf-8') 
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s : %(message)s',
                                           datefmt='%Y/%m/%d %H:%M:%S')) 
    logger.addHandler(handler)
    return logger

def stringToBoolean(v):
    """ convertit une chaine de caractère en booleen """
    return v.lower() in ("true", "1")


def getInt(message,mini, maxi):
    """
    Demande à l'utilisateur un entier entre deux valeurs incluses et la retourne
    la demande est réeffectuée tant que la saisie ne correspond pas aux critères
    """
    while True:
        try:
            nombre_saisi=int(input(message))            
            #si le nombre saisi est un entier correspondant aux critÃ¨res on quitte la boucle infini
            if nombre_saisi>=mini and nombre_saisi<=maxi:
                return nombre_saisi
            print('Saisissez un entier entre '+str(mini)+' et '+str(maxi))
        #si la saisi n'est pas un entier, affichage erreur et retour au dÃ©but la boucle infini
        except ValueError:
            print('Saisissez un entier entre '+str(mini)+' et '+str(maxi))

def getValue(message,data=[]):
    """
    Demande à l'utilisateur une valeur incluse dans un tableau de donnée s'il est spécifié et la retourne
    la demande est réeffectuée tant que la saisie ne correspond pas aux critères éventuels
    """ 
    while True:
        valeur_saisie=input(message)
        #si le nombre saisi est un entier correspondant aux critÃ¨res on quitte la boucle infini
        if(len(data)==0 or valeur_saisie in data):
            return valeur_saisie

def askChoice(message,choices):
    """ 
    affiche une message et une liste de choix et demande une des valeurs à l'utilisateur 
    retourne un entier correspondant l'index du tableau choices
    """
    print(message)
    for i in range(0,len(choices)):
        print(str(i+1)+" : "+choices[i])
    return getInt("Votre Choix: ",1,len(choices))-1

def askBoolean(message):
    value = confirm("\n" + message +" (y/n) : ")
    if value == 'y':
        return True
    else:
        return False

def confirm(message,tableau=[]):
    """
    Demande à l'utilisateur de saisir des informations et demande une confirmation
    Affiche un message et une eventuelle liste de choix
    La demande boucle tant qu'une valeur n'est pas confirmée
    """
    while True:
        if (len(tableau)==0):
            reponse=getValue(message)
        else:
            reponse = tableau[askChoice(message,tableau)]            
        confirm = getValue("Confirmez-vous votre choix : "+reponse+" ? (y/n) : ",["y","n"])
        if (confirm=="y"):
            return reponse
        else:
            continue

def deletePath(backupFilePath):
    """
    Supprimme un fichier et son dossier parent s'il est vide
    """
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