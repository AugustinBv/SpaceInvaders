import tkinter as t
from tkinter.constants import LEFT, RIGHT
from random import randint
import interract


# Constantes

framerate = 30

borderPadding = 5
spawnPadding = 50
alienPadding = 10

alienSpeed = 3
alienSize = 15
alienHealth = 1

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

ennemies = interract.ennemies(si, framerate, borderPadding, alienSpeed)

nAlien = 56
counter = 0
xOffset = spawnPadding
yOffset = 20

while counter < nAlien:

    if( xOffset + alienPadding + alienSize > 800 - spawnPadding):
        xOffset = spawnPadding
        yOffset += 20
    alien1 = interract.alien(screen,[xOffset,yOffset],alienSize,alienHealth,ennemies)
    xOffset += alienPadding + alienSize
    counter += 1


ennemies.moveAliens()


si.mainloop()