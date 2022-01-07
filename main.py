import tkinter as t
from tkinter.constants import LEFT, RIGHT
from random import randint
import interract


#Création de la fenêtre
si = t.Tk()
si.title('Space Invaders')
si["bg"]="grey"
largeur, hauteur = 800, 600
lab = t.Label(si)
lab["text"]="score : "  #faire un score qui évolue
lab.pack()

#Widget jeu
screen = t.Canvas(si, width = largeur, height = hauteur, bg = 'black')
screen.pack(side = LEFT, padx = 5, pady = 5)

#widget bouton quitter
buttonQuit = t.Button(si, text = "Quitter", fg = "red", command =si.destroy)
buttonQuit.pack(side = RIGHT, padx = 5, pady = 5)

#widget bouton menu
buttonMenu = t.Button(si, text = "Menu", fg = "red")
buttonMenu.pack(side = RIGHT, padx = 5, pady = 5)

alien1 = interract.alien(0,1,10,10)


si.mainloop()