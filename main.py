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
ALIENYMOVE = 20
ALIENSHOOTINGCHANCE = 0.01
SHOOTINGALIENPROPORTION = 0.2

NALIEN = 20

ENTITIESTYPES = ["player","alien","wall","laser"]

#Création de la fenêtre
window = t.Tk()

window.title('Space Invaders')
window["bg"]="grey"
largeur, hauteur = 800, 600



# Separation de la fenetre

leftFrame = t.Frame(window)  # Moitiée gauche
leftFrame.grid(row = 0,column=0)
rightFrame = t.Frame(window) # Moitiée droite
rightFrame.grid(row = 0, column=1)

# Widget Label de score
scoreText = t.StringVar()
scoreText.set("score : 0      vies : 3")
scoreLabel = t.Label(leftFrame,textvariable = scoreText)
scoreLabel.grid(row= 0, column=0, padx= 5, pady= 5)


# Widget canvas de jeu
canvas = t.Canvas(leftFrame, width = largeur, height = hauteur, bg = 'black')
canvas.grid(row= 1, column=0, padx= 5, pady= 5)
canvas.focus_set()

# Widget bouton start
buttonStart = t.Button(rightFrame, text = "  Start  ", fg = "red")
buttonStart.grid(row=0, column=0, padx= 5, pady= 5)


# Widget bouton menu
#buttonMenu = t.Button(rightFrame, text = "Menu", fg = "red")
#buttonMenu.grid(row=1, column=0, padx= 5, pady= 5)

# Widget bouton quitter
buttonQuit = t.Button(rightFrame, text = "Quitter", fg = "red", command =window.destroy)
buttonQuit.grid(row= 2, column=0, padx= 5, pady= 5)


options = interract.GameOptions(FRAMERATE,BORDERPADDING,ALIENSPEED,ALIENSIZE, ALIENYMOVE,ENTITIESTYPES,
 ALIENSHOOTINGCHANCE, SHOOTINGALIENPROPORTION, NALIEN,SPAWNPADDING,ALIENPADDING)

gameManager = interract.Game(options, window, canvas, 3, scoreText)


buttonStart.configure(command= gameManager.Restart)

canvas.bind("<<GameStarted>>", lambda event: buttonStart.configure(text="Restart"))   

window.mainloop()