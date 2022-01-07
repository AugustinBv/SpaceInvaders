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
leftFrame = t.Frame()
leftFrame.grid(row = 0,column=0)
rightFrame = t.Frame()
rightFrame.grid(row = 0, column=1)

#Widget label de score
lab = t.Label(leftFrame)
lab["text"]="score : "  #faire un score qui évolue
lab.grid(row= 0, column=0, padx= 5, pady= 5)

#Widget fenetre de jeu
screen = t.Canvas(leftFrame, width = largeur, height = hauteur, bg = 'black')
screen.grid(row= 1, column=0, padx= 5, pady= 5)


#widget bouton start
startMenu = t.Button(rightFrame, text = "Start", fg = "red")
startMenu.grid(row=0, column=0, padx= 5, pady= 5)

#widget bouton menu
buttonMenu = t.Button(rightFrame, text = "Menu", fg = "red")
buttonMenu.grid(row=1, column=0, padx= 5, pady= 5)

#widget bouton quitter
buttonQuit = t.Button(rightFrame, text = "Quitter", fg = "red", command =si.destroy)
buttonQuit.grid(row= 2, column=0, padx= 5, pady= 5)



si.mainloop()