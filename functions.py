import os
import pymysql
from tkinter import TclError,messagebox
from backupOptions import BackupOption

#fonction permettant de centrer une fenêtre sur l'écran
def centerFrame(frame):
    frame.withdraw()
    frame.update_idletasks()
    x = (frame.winfo_screenwidth() - frame.winfo_reqwidth()) / 2
    y = (frame.winfo_screenheight() - frame.winfo_reqheight()) / 2
    frame.geometry("+%d+%d" % (x, y))
    frame.deiconify()

#affiche un message dans une pop up ou en console suivant les ressources du système
def display(title,message):    
    try:
        messagebox.showerror(title, message)
    except TclError as e:
        print("----"+title+"----")
        print(message)
        

def displayMessage(message):
    display("Information", message)

def displayError(message):
    display("Erreur", message)



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

if __name__=="__main__":
    call()