import tkinter as t
from tkinter.constants import LEFT, RIGHT
from random import randint
from functools import partial
import interract



# Constantes

framerate = 30

borderPadding = 5
spawnPadding = 50
alienPadding = 10

alienSpeed = 3
alienSize = 15
alienHealth = 1
yAlienDeplacement = 20

nAlien = 56


global score
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

#Widget scoreLabelel de score
scoreText = t.StringVar()
scoreText.set("12")
scoreLabel = t.Label(leftFrame,textvariable = scoreText)
scoreLabel.grid(row= 0, column=0, padx= 5, pady= 5)


#Widget fenetre de jeu
screen = t.Canvas(leftFrame, width = largeur, height = hauteur, bg = 'black')
screen.grid(row= 1, column=0, padx= 5, pady= 5)
screen.focus_set()

#widget bouton start
buttonStart = t.Button(rightFrame, text = "Start", fg = "red")
buttonStart.grid(row=0, column=0, padx= 5, pady= 5)


#widget bouton menu
buttonMenu = t.Button(rightFrame, text = "Menu", fg = "red")
buttonMenu.grid(row=1, column=0, padx= 5, pady= 5)

#widget bouton quitter
buttonQuit = t.Button(rightFrame, text = "Quitter", fg = "red", command =si.destroy)
buttonQuit.grid(row= 2, column=0, padx= 5, pady= 5)


entities = interract.entities(si, framerate, borderPadding, alienSpeed, yAlienDeplacement)

counter = 0
xOffset = spawnPadding
yOffset = 20

while counter < nAlien:
    if( xOffset + alienPadding + alienSize > 800 - spawnPadding):
        xOffset = spawnPadding
        yOffset += 20
    alien1 = interract.alien(screen,[xOffset,yOffset],alienSize,alienHealth,entities)
    xOffset += alienPadding + alienSize
    counter += 1

itsMeMario = interract.player(screen,[400,550],20,5,3,entities,scoreText)
screen.bind('<Right>', itsMeMario.bougeSTP)
screen.bind('<Left>', itsMeMario.bougeSTP)
screen.bind('<Key>', itsMeMario.keys)


entities.moveAliens()
itsMeMario.checkForCollisionWithAliens()



si.mainloop()