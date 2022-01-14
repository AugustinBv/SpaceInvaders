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
yAlienDeplacement = 10

nAlien = 56

# Variables



# fonctions

def startGame(screenSG, ennemiesSG):


    counter = 0
    xOffset = spawnPadding
    yOffset = 20

    while counter < nAlien:
        if( xOffset + alienPadding + alienSize > 800 - spawnPadding):
            xOffset = spawnPadding
            yOffset += 20
        alien1 = interract.alien(screenSG,[xOffset,yOffset],alienSize,alienHealth,ennemiesSG)
        xOffset += alienPadding + alienSize
        counter += 1

    itsMeMario = interract.player(screenSG,[400,550],20,5,50)
    screenSG.bind('<Right>', itsMeMario.bougeSTP)
    screenSG.bind('<Left>', itsMeMario.bougeSTP)
    screenSG.bind('<Key>', itsMeMario.keys)

    ennemiesSG.moveAliens()
    gameRunning = True



#Création de la fenêtre
si = t.Tk()

si.title('Space Invaders')
si["bg"]="grey"
largeur, hauteur = 800, 600


ennemies = interract.ennemies(si, framerate, borderPadding, alienSpeed, yAlienDeplacement)



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
buttonStart = t.Button(rightFrame, text = "Start", fg = "red",command=partial(startGame,screen,ennemies))
buttonStart.grid(row=0, column=0, padx= 5, pady= 5)


#widget bouton menu
buttonMenu = t.Button(rightFrame, text = "Menu", fg = "red")
buttonMenu.grid(row=1, column=0, padx= 5, pady= 5)

#widget bouton quitter
buttonQuit = t.Button(rightFrame, text = "Quitter", fg = "red", command =si.destroy)
buttonQuit.grid(row= 2, column=0, padx= 5, pady= 5)





si.mainloop()