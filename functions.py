import os
from tkinter import TclError,messagebox
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
    if(os.isatty(sys.stdin.fileno())):
        if (title!=""): print("----"+title+"----")
        print(message)
    else:
        messagebox.showinfo(title, message)

def displayInfo(message):
    """ affiche un message dans une pop up ou en console suivant les ressources du système et enregistre le message dans les logs """    
    display(message,"Information")
    initLog().info(message)

def displayError(message):
    """ affiche une erreur dans une pop up ou en console suivant les ressources du système et enregistre le message dans les logs """
    if(os.isatty(sys.stdin.fileno())):
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
            #si le nombre saisi est un entier correspondant aux critères on quitte la boucle infini
            if nombre_saisi>=mini and nombre_saisi<=maxi:
                return nombre_saisi
            print('Saisissez un entier entre '+str(mini)+' et '+str(maxi))
        #si la saisi n'est pas un entier, affichage erreur et retour au début la boucle infini
        except ValueError:
            print('Saisissez un entier entre '+str(mini)+' et '+str(maxi))

def getValue(message,data=[]):
    """
    Demande à l'utilisateur une valeur incluse dans un tableau de donnée s'il est spécifié et la retourne
    la demande est réeffectuée tant que la saisie ne correspond pas aux critères éventuels
    """ 
    while True:
        valeur_saisie=input(message)
        #si le nombre saisi est un entier correspondant aux critères on quitte la boucle infini
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
    return getInt("Votre Choix ? : ",1,len(choices))-1

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

'''            
def call(host='162.243.164.132',user='jules',password='jules',db='backupTest'):
    try:
        connection = pymysql.connect(host=host, user=user, password=password,
            charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        
        os.chdir("C:\\wamp\\bin\\mysql\\mysql5.6.17\\bin")
        cmd="mysqldump -h "+host+" -u "+user+" -p"+password+" "+ db +" > D:\\a\\backupTest.sql"
        print(cmd)
        output = os.system(cmd)
        
        
        if (output==2):
            try:
                messagebox.showerror("Erreur", "Vous ne disposez pas des droits nécessaires pour effectuer une sauvegarde")
            except TclError as e:
                print("Vous ne disposez pas des droits nécessaires pour effectuer une sauvegarde")
        elif(output==1):
            try:
                messagebox.showerror("Erreur", "Erreur de la requête. Vérifiez que mysqldump est installé")
            except TclError as e:
                print ("Erreur de la requête. Vérifiez que mysqldump est installé")
        elif(output!=0):
            #pour le debugage et retour utilisateur                    
            try:
                messagebox.showerror("Erreur", "output = "+str(output)+" - Une erreur est survenue!")
            except TclError as e:
                print("output =",output,"- Une erreur est survenue!")
        connection.close()
    except pymysql.err.OperationalError as e1:
        if(e1.args[0]==2003):
            try:
                messagebox.showerror("Erreur", "Impossible de se connecter au serveur")
            except TclError as e:
                print("Impossible de se connecter au serveur")
        elif(e1.args[0]==1044):
            try:
                messagebox.showerror("Erreur", "Acces refusé! Vous ne disposez pas des droits nécessaire d'accès à la base")
            except TclError as e:
                print("Acces refusé! Vous ne disposez pas des droits nécessaire d'accès à la base")
    except pymysql.err.InternalError as e2:
        if(e2.args[0]==1049):
            try:
                messagebox.showerror("Erreur", "La base de données n'éxiste pas")
            except TclError as e:
                print("La base de données n'éxiste pas")
    except Exception as e3:
        #pour le debugage et retour utilisateur                    
        try:
            messagebox.showerror("Erreur", e3.args)
        except TclError as e:
            print(e3.args)
'''

if __name__=="__main__":
    #call()
    print (getInt("Votre choix : ",1,5))
    print (getValue("Confimez-vous : ",["y","n"]))

