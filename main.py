import tkinter as t
from tkinter.constants import LEFT, RIGHT
from random import randint
from functools import partial
import interract
import time



# Constantes

framerate = 75

borderPadding = 5
spawnPadding = 50
alienPadding = 10

alienSpeed = 3
alienSize = 15
alienHealth = 1
yAlienDeplacement = 20

nAlien = 56

entitiesTypes = ["player","alien","wall","laser"]

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


entities = interract.entities(si, framerate, borderPadding, alienSpeed, yAlienDeplacement, entitiesTypes)

counter = 0
xOffset = spawnPadding
yOffset = 20

while counter < nAlien:
    if( xOffset + alienPadding + alienSize > 800 - spawnPadding):
        xOffset = spawnPadding
        yOffset += 20
    alien1 = interract.alien(screen,[xOffset,yOffset],alienSize,alienHealth,entities,entitiesTypes[1])
    xOffset += alienPadding + alienSize
    counter += 1

itsMeMario = interract.player(screen,[400,550],20,10,3,entities,scoreText,entitiesTypes[0], 0.3)
screen.bind('<Right>', itsMeMario.bougeSTP)
screen.bind('<Left>', itsMeMario.bougeSTP)
screen.bind('<Key>', itsMeMario.keys)
screen.bind('<space>', lambda event : itsMeMario.shoot(2,1,15,event))


entities.moveAliens()
entities.moveLaser()
itsMeMario.checkForCollisionWithAliens()



si.mainloop()