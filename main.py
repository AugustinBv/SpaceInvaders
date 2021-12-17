import tkinter as t
from tkinter.constants import LEFT, RIGHT
from random import randint


#Création de la fenêtre
si = t.Tk()
si.title('Space Invaders')
si["bg"]="grey"
largeur, hauteur = 800, 600
lab = t.Label(si)
lab.pack()

def gameLoop():
    lab["text"]= si.winfo_width()
    si.after(100, gameLoop)

#Widget jeu
screen = t.Canvas(si, width = largeur, height = hauteur, bg = 'black')
screen.pack(side = LEFT, padx = 5, pady = 5)

#widget bouton quitter
buttonQuit = t.Button(si, text = "Quitter", fg = "red", command =si.destroy)
buttonQuit.pack(side = RIGHT, padx = 5, pady = 5)

#widget bouton menu
buttonMenu = t.Button(si, text = "Menu", fg = "red")
buttonMenu.pack(side = RIGHT, padx = 5, pady = 5)

si.after(100, gameLoop)

print("Hello world")

si.mainloop()