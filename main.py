import tkinter as t
from tkinter.constants import LEFT, RIGHT
from random import randint
from functools import partial
import interract
import time



# Constantes

FRAMERATE = 75

BORDERPADDING = 5
SPAWNPADDING = 50
ALIENPADDING = 20

ALIENSPEED = 2
ALIENSIZE = 15
ALIENSPEED = 1
YALIENMOVE = 20

NALIEN = 20

ENTITIESTYPES = ["player","alien","wall","laser"]

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


entities = interract.entities(si, FRAMERATE, BORDERPADDING, ALIENSPEED, YALIENMOVE, ENTITIESTYPES)

counter = 0
xOffset = SPAWNPADDING
yOffset = 20

while counter < NALIEN:
    if( xOffset + ALIENPADDING + ALIENSIZE > 800 - SPAWNPADDING):
        xOffset = SPAWNPADDING
        yOffset += 20
    alien1 = interract.alien(screen,[xOffset,yOffset],ALIENSIZE,ALIENSPEED,entities,ENTITIESTYPES[1])
    xOffset += ALIENPADDING + ALIENSIZE
    counter += 1

itsMeMario = interract.player(screen,[400,550],20,10,3,entities,scoreText,ENTITIESTYPES[0], 0.3)
screen.bind('<Right>', itsMeMario.bougeSTP)
screen.bind('<Left>', itsMeMario.bougeSTP)
screen.bind('<Key>', itsMeMario.keys)
screen.bind('<space>', lambda event : itsMeMario.shoot(2,1,15,event))


entities.moveAliens()
entities.moveLaser()
itsMeMario.checkForCollisionWithAliens()



si.mainloop()