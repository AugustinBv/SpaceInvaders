import tkinter as t
from tkinter.constants import LEFT, RIGHT
from random import randint
import interract


#Création de la fenêtre
si = t.Tk()

si.title('Space Invaders')
si["bg"]="grey"
largeur, hauteur = 800, 600

#Separation de la fenetre
leftFrame = t.Frame(si)
leftFrame.grid(row = 0,column=0)
rightFrame = t.Frame(si)
rightFrame.grid(row = 0, column=1)

#Widget label de score
lab = t.Label(leftFrame)
lab["text"]="score : "  #faire un score qui évolue
lab.grid(row= 0, column=0, padx= 5, pady= 5)

#Widget fenetre de jeu
screen = t.Canvas(leftFrame, width = largeur, height = hauteur, bg = 'black')
screen.grid(row= 1, column=0, padx= 5, pady= 5)
screen.focus_set()

#widget bouton start
startMenu = t.Button(rightFrame, text = "Start", fg = "red")
startMenu.grid(row=0, column=0, padx= 5, pady= 5)

#widget bouton menu
buttonMenu = t.Button(rightFrame, text = "Menu", fg = "red")
buttonMenu.grid(row=1, column=0, padx= 5, pady= 5)

#widget bouton quitter
buttonQuit = t.Button(rightFrame, text = "Quitter", fg = "red", command =si.destroy)
buttonQuit.grid(row= 2, column=0, padx= 5, pady= 5)

#screen.create_oval(50,50,70,70,outline='red',fill='red')


alien1 = interract.alien(si,screen,[50,50],10,1,10)
alien2 = interract.alien(si,screen,[70,50],10,1,10)
itsMeMario = interract.player(si,screen,[400,550],20,5,50)
screen.bind('<Right>', itsMeMario.bougeSTP)
screen.bind('<Left>', itsMeMario.bougeSTP)
screen.bind('<Key>', itsMeMario.keys)

alien1.applySpeed()
alien2.applySpeed()


si.mainloop()