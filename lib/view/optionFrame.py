#!/usr/bin/python3
# -*-coding:utf-8 -*

from tkinter import Tk,Frame,Toplevel,Canvas,LabelFrame,Label,Entry,Button,Checkbutton,OptionMenu,END,IntVar,StringVar
from lib.utils.functions import centerFrame, displayError
from lib.utils.compress import getCompressTypeList
from lib.entity.backupFactory import BackupFactory
    
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
        
        self.sgbd = StringVar()
        supportedSGBD = BackupFactory.getSupportedSGBD()
        
        self.sgbdList = OptionMenu(self.canevas, self.sgbd,*supportedSGBD)
        self.sgbd.set(supportedSGBD[0])        
        self.sgbdList.config(width=23)
        self.sgbdList.grid(row=i,column=j+1,columnspan=2,padx=5,pady=0)
        
        i=i+1
        #hôte
        labelHote = Label(self.canevas, text="Hote : ")
        labelHote.grid(row=i,column=j,columnspan=1,padx=10,pady=10,sticky="e")
        self.host = StringVar()
        self.host.set("localhost")
        self.inputHote = Entry(self.canevas, width=30, textvariable=self.host)
        self.inputHote.grid(row=i,column=j+1,columnspan=2,padx=5,pady=10)
        
        i=i+1
        #port
        labelPort = Label(self.canevas, text="Port : ")
        labelPort.grid(row=i,column=j,columnspan=1,padx=10,pady=10,sticky="e")
        self.port = IntVar()
        self.port.set(3306)
        self.inputPort = Entry(self.canevas, width=30, textvariable=self.port)
        self.inputPort.grid(row=i,column=j+1,columnspan=2,padx=5,pady=10)
        
        i=i+1
        #nom utilisateur
        self.user = StringVar()
        labelUtil = Label(self.canevas, text="Utilisateur : ")
        labelUtil.grid(row=i,column=j,columnspan=1,padx=5,pady=10,sticky="e")   
        self.inputUtil = Entry(self.canevas, width=30,textvariable=self.user)
        self.inputUtil.grid(row=i,column=j+1,columnspan=2,padx=5,pady=10)
        
        i=i+1
        #mot de passe
        self.pwd = StringVar()
        labelPwd = Label(self.canevas, text="Mot de passe : ")
        labelPwd.grid(row=i,column=j,columnspan=1,padx=5,pady=10,sticky="e")
        self.inputPwd = Entry(self.canevas,show="*", width=30,textvariable=self.pwd)
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
        self.allDatabases = IntVar()
        checkBut = Checkbutton(self.canevas,text="Toutes les bases",variable=self.allDatabases,command=self.updateInputDb)
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
        self.compressType = StringVar()
        compressList = getCompressTypeList()
        self.compressionTypeList = OptionMenu(paramFrame, self.compressType, *compressList)
        self.compressType.set(compressList[0])
        self.compressionTypeList.config(width=4)
        self.compressionTypeList.config(state='disable')
        self.compressionTypeList.grid(row=iParam,column=jParam+1,columnspan=1,padx=5,pady=0)
        
        
        iParam=iParam+1
        #case à cocher pour le cryptage
        self.crypt = IntVar()
        cryptCheckBut = Checkbutton(paramFrame,text="Crypter",variable=self.crypt,command=self.askKey)
        cryptCheckBut.grid(row=iParam,column=jParam,columnspan=1,padx=5,pady=0,sticky="w")
        
        
        i=i+1
        
        butFrame = Frame(self.canevas)
        butFrame.grid( row=i, column=0,columnspan=3,padx=5, pady=10)
        
        #boutton de validation
        self.exeBtn=Button(butFrame,text='Executer', command=self.validAction)
        self.exeBtn.grid(row=0,column=0,columnspan=1,padx=5,pady=10)
                               
        #boutton quitter
        self.quitBtn=Button(butFrame,text='Quitter', command=self.destroy)
        self.quitBtn.grid(row=0,column=1,columnspan=1,padx=5,pady=10)
        
        self.canevas.pack()
            
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
        # si toute les bases sont selectionnées, on affiche une étoile et on desactive le bouton ajouter
        # sinon la liste des bases et on active le bouton ajouter
        if(self.allDatabases.get()):
            self.inputDb.insert(0,"*")
            self.inputDb.config(state='disable')
            self.addBtn.config(state='disable')
        else:
            self.inputDb.insert(0, self.options.databases)
            self.inputDb.config(state='readonly')
            self.addBtn.config(state='normal')
    
    #affichage de la fenetre
    def show(self):
        self.mainloop() 
    
    #affichage d'une fenetre pour choisir les BDD
    def showDbChoiceFrame(self):
        #si la fenetre n'est pas ouverte
        if(not self.choiceWindowOpen):
            #MAJ des données saisies et recupération de la liste des BDD
            self.updateOptions()
            backup = BackupFactory.create(self.options)                
            databases =  backup.getDatabases()
            if(len(databases)>0):
                #affichage d'une fentre'
                self.choiceWindowOpen=True
                self.choiceDbWindow = Toplevel(self.master)
                self.choiceDbWindow.protocol("WM_DELETE_WINDOW", self.cancelChange)
                self.choiceDbFrame = Frame(self.choiceDbWindow)
                self.choiceDbWindow.title("BDD")
                self.databasesList=[]
                self.enable=[]
                #création des varibles résultat pour chaque base stocké dans un tableau enable[]
                for database in databases:
                    self.databasesList.append(database)
                    self.enable.append(IntVar())
                    if(database in self.options.databases):
                        self.enable[-1].set(1)
                    else:
                        self.enable[-1].set(0)
                row=0
                #creation d'un checkbox par base de données
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
                
    #MAJ des saisie utilisateur dans l'objet BackupOption
    def updateOptions(self):
        self.options.sgbd = self.sgbd.get()
        self.options.host = self.host.get()
        self.options.port = self.port.get()
        self.options.user = self.user.get()
        self.options.pwd = self.pwd.get()
        self.options.allDatabases = self.allDatabases.get()
        self.options.compressType = self.compressType.get()
        self.options.crypt = self.crypt.get()
        if(self.allDatabases.get()):
            backup = BackupFactory.create(self.options)
            self.options.databases =  backup.getDatabases()
        
                         
    def validChoice(self):
        #on verifie les checkbox selectionner
        # en fonction on les ajoute ou les supprimme de la liste
        for i in range(0,len(self.databasesList)):
            if(self.enable[i].get()):
                self.options.addDatabase(self.databasesList[i])
            else:
                self.options.removeDatabase(self.databasesList[i])
        #destruction de la fenetre
        self.choiceWindowOpen=False   
        self.choiceDbWindow.destroy()
        self.updateInputDb()
    
    def cancelChange(self):
        self.choiceWindowOpen=False
        self.choiceDbWindow.destroy()
    
    #ouverture d'une popup pour saisir la clé de cryptage
    def askKey(self):
        self.updateOptions()
        if(self.options.crypt):
            #construction de la popup
            self.popup=Toplevel(self.master)
            self.popup.title("Clé")
            label=Label(self.popup,text="Entrez la clé de cryptage")
            label.pack()
            self.keyEntry=Entry(self.popup,show="*",width=30)
            self.keyEntry.insert(0, self.options.cryptKey)
            self.keyEntry.pack()
            button=Button(self.popup,text='Ok',command=self.setCryptKey)
            button.pack()
            #on cache la fenetre principale
            self.withdraw()
            #on centre la popup
            centerFrame(self.popup)
            #on attend la reponse de la popup
            self.wait_window(self.popup)
            #on reaffiche la fenetre principale et on detruit la popup
            self.deiconify()
            self.popup.destroy()
    
    #MAJ de la clé de cryptage
    def setCryptKey(self):
        self.options.cryptKey = self.keyEntry.get()
        self.popup.destroy()
        
    #validation des options
    def validAction(self):
        self.updateOptions()
        try:
            backup = BackupFactory.create(self.options)
            backup.execute()
        except Exception as e:
            displayError(e.args[1])
