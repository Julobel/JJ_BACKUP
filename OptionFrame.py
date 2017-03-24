#!C:\Users\JB\AppData\Local\Programs\Python\Python35-32\python.exe
from tkinter import Tk,Frame,Toplevel,Canvas,LabelFrame,Label,Entry,Button,Checkbutton,OptionMenu,END,IntVar,StringVar,messagebox
from functions import centerFrame
from compress import compressFile
from backupOptions import BackupOption
import pymysql
    
class OptionFrame(Tk): 
    def __init__(self,options):
        Tk.__init__(self)
        self.title("Choisissez vos options")
        self.canevas=Canvas(self)
        self.choiceWindowOpen = False
        self.options = options
        self.build()
        centerFrame(self)
    
    #positionnement des éléments de la fenêtre
    def build(self):
        i=0
        j=0
        
                
        #liste des SGBD
        labelHote = Label(self.canevas, text="SGBD : ")
        labelHote.grid(row=i,column=j,columnspan=1,padx=10,pady=10,sticky="e")
        self.options.sgbd = StringVar()
        self.options.sgbd.set(BackupOption.SGBD_MYSQL)        
        self.sgbdList = OptionMenu(self.canevas, self.options.sgbd, 
                                   BackupOption.SGBD_MYSQL, 
                                   BackupOption.SGBD_ORACLE,
                                   BackupOption.SGBD_SQLSERVER, 
                                   BackupOption.SGBD_POSTGRE,
                                   BackupOption.SGBD_SQLLITE)
        self.sgbdList.config(width=23)
        self.sgbdList.grid(row=i,column=j+1,columnspan=2,padx=5,pady=0)
        
        i=i+1
        #hôte
        labelHote = Label(self.canevas, text="Hote : ")
        labelHote.grid(row=i,column=j,columnspan=1,padx=10,pady=10,sticky="e")
        self.options.host = StringVar()
        self.inputHote = Entry(self.canevas, width=30, textvariable=self.options.host)
        self.options.host.set("localhost")
        self.inputHote.grid(row=i,column=j+1,columnspan=2,padx=5,pady=10)
        
        i=i+1
        #nom utilisateur
        self.options.user = StringVar()
        labelUtil = Label(self.canevas, text="Utilisateur : ",textvariable=self.options.user)
        labelUtil.grid(row=i,column=j,columnspan=1,padx=5,pady=10,sticky="e")   
        self.inputUtil = Entry(self.canevas, width=30)
        self.inputUtil.grid(row=i,column=j+1,columnspan=2,padx=5,pady=10)
        
        i=i+1
        #mot de passe
        self.options.pwd = StringVar()
        labelPwd = Label(self.canevas, text="Mot de passe : ",textvariable=self.options.pwd)
        labelPwd.grid(row=i,column=j,columnspan=1,padx=5,pady=10,sticky="e")
        self.inputPwd = Entry(self.canevas,show="*", width=30)
        self.inputPwd.grid(row=i,column=j+1,columnspan=2,padx=5,pady=10)
        
        
        i=i+1
        #affichage des bases choisies
        labelDB = Label(self.canevas, text="Nom de la base : ")
        labelDB.grid(row=i,column=j,columnspan=1,padx=5,pady=10,sticky="e")
        self.inputDb = Entry(self.canevas, width=20,state='readonly')
        self.inputDb.grid(row=i,column=j+1,columnspan=1,padx=5,pady=10)
        self.addBtn=Button(self.canevas,text='Ajouter', command=self.showDbChoiceFrame)
        self.addBtn.grid(row=i,column=j+2,columnspan=1,padx=5,pady=10)
        
        i=i+1
        self.options.allDatabases = IntVar()
        checkBut = Checkbutton(self.canevas,text="Toutes les bases",variable=self.options.allDatabases,command=self.changeAllDbState)
        checkBut.grid(row=i,column=1,columnspan=1,padx=5,pady=0,sticky="w")
        
        i=i+1
        #paramètres avancés : compression et cryptage
        paramFrame = LabelFrame(self.canevas, text="Paramètres avancés")
        paramFrame.grid( row=i, column=j,columnspan=3,padx=5, pady=10)
                
        iParam=0
        jParam=0
        #case à cocher pour la compression
        self.compress = IntVar()
        compressCheckBut = Checkbutton(paramFrame,text="Compresser",variable=self.compress,command=self.changeCompressState)
        compressCheckBut.grid(row=iParam,column=jParam,columnspan=1,padx=5,pady=0,sticky="w")
        
        #liste des type de compression qui s'active uniquement lorsque l'option compression est cochée
        self.options.compressType = StringVar()
        self.options.compressType.set("zip")
        self.compressionTypeList = OptionMenu(paramFrame, self.options.compressType, "zip", "gz", "bz2")
        self.compressionTypeList.config(width=4)
        self.compressionTypeList.config(state='disable')
        self.compressionTypeList.grid(row=iParam,column=jParam+1,columnspan=1,padx=5,pady=0)
        
        
        iParam=iParam+1
        #case à cocher pour le cryptage
        self.options.crypt = IntVar()
        compressCheckBut = Checkbutton(paramFrame,text="Crypter",variable=self.options.crypt)
        compressCheckBut.grid(row=iParam,column=jParam,columnspan=1,padx=5,pady=0,sticky="w")
        
        i=i+1
        #boutton de validation
        self.validBtn=Button(self.canevas,text='Valider', command=self.validAction)
        self.validBtn.grid(row=i,column=0,columnspan=3,padx=5,pady=10)
                
        self.canevas.pack()
    
    #active ou desactive le chanmp du nom des BDD
    def changeAllDbState(self):
        if(self.options.allDatabases.get()):
            self.inputDb.config(state='disable')
            self.addBtn.config(state='disable')
        else:
            self.inputDb.config(state='readonly')
            self.addBtn.config(state='normal')
            
    #active ou desactive le choix de la compression        
    def changeCompressState(self):
        if(self.compress.get()):
            self.compressionTypeList.config(state='normal')
        else:
            self.compressionTypeList.config(state='disable')
            
    #mise à jour de l'input avec les base de données
    def updateInputDb(self):
        #reactivation et suppression du texte
        self.inputDb.config(state='normal')
        self.inputDb.delete(0, END)
        # si toute les base sont selectionnés, on affiche une étoile
        # sinon la list des base
        if(self.options.allDatabases.get()):
            self.inputDb.insert(0,"*")
            self.inputDb.config(state='disable')
        else:
            self.inputDb.insert(0, self.options.databases)
            self.inputDb.config(state='readonly')
            
    def show(self):
        self.mainloop() 
    
    def showDbChoiceFrame(self):
        if(not self.choiceWindowOpen):
            self.choiceWindowOpen=True
            self.choiceDbWindow = Toplevel(self.master)
            self.choiceDbWindow.protocol("WM_DELETE_WINDOW", self.cancelChange)
            self.choiceDbFrame = Frame(self.choiceDbWindow)
            try:
                connection = pymysql.connect(host=self.inputHote.get(), user=self.inputUtil.get(), password=self.inputPwd.get(),
                    charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
                self.choiceDbWindow.title("BDD")
                self.databasesList=[]
                self.enable=[]
                
                cursor = connection.cursor()
                cursor.execute('SHOW DATABASES')
                database = cursor.fetchone()
                connection.close()
                while database:
                    self.databasesList.append(database['Database'])
                    self.enable.append(IntVar())
                    if(database['Database'] in self.options.databases):
                        self.enable[-1].set(1)
                    else:
                        self.enable[-1].set(0)
                    database = cursor.fetchone()
                    
                row=0
                for i in range(0,len(self.databasesList)):
                    #case à cocher pour chaque base
                    checkBut = Checkbutton(self.choiceDbFrame,text=self.databasesList[i],variable=self.enable[i])
                    checkBut.grid(row=row,column=0,columnspan=1,padx=5,pady=0,sticky="w")
                    row=row+1
                
                #boutton de validation
                dbChoiceFrameValidBtn=Button(self.choiceDbFrame,text='Valider',command=self.validChoice)
                dbChoiceFrameValidBtn.grid(row=row,column=0,columnspan=3,padx=5,pady=10)  
                        
                self.choiceDbFrame.pack()            
                centerFrame(self.choiceDbWindow)
            except pymysql.err.OperationalError as e1:
                if(e1.args[0]==2003):
                    messagebox.showerror("Erreur", "Impossible de se connecter au serveur : "+self.inputHote.get())   
                     
    def validChoice(self):
        #on verifie les checkbox selectionner
        # en fonction on les ajoute ou les supprimme de la liste
        for i in range(0,len(self.databasesList)):
            if(self.enable[i].get()):
                self.options.addDatabe(self.databasesList[i])
            else:
                self.options.removeDatabe(self.databasesList[i])
        #destruction de la fenetre
        self.choiceWindowOpen=False   
        self.choiceDbWindow.destroy()
        self.updateInputDb()
    
    def cancelChange(self):
        self.choiceWindowOpen=False   
        self.choiceDbWindow.destroy()
        
    
    #validation des options
    def validAction(self):            
        #for i in range(0,len(self.options.databases)):
        #    print(self.options.databases[i])
        if (self.options.sgbd.get()==BackupOption.SGBD_MYSQL):
            try:
                self.destroy()
            except:
                pass
        else:
            messagebox.showerror("Erreur", "Ce SGBD n'est pas géré.")


if __name__=="__main__":    
    hFrame = OptionFrame()
    hFrame.show()


