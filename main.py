import tkinter as t
from tkinter.constants import LEFT, RIGHT
from random import randint
from functools import partial
from tkinter.ttk import Label
import interract
import time



# Constantes

FRAMERATE = 75
CANVAS_SIZE = 800, 600

BORDER_PADDING = 5
SPAWN_PADDING = 50
ALIEN_PADDING = 20

ALIEN_SPEED = 2
ALIEN_SIZE = 15
ALIEN_Y_MOVE = 10
ALIEN_SHOOTING_CHANCE = 0.01
SHOOTING_ALIEN_PROPORTION = 0.2

N_ALIEN = 20
N_WALLS = 10

ENTITIES_TYPES = ["player","alien","wall","laser"]

#Création de la fenêtre
window = t.Tk()

window.title('Space Invaders')
window["bg"]="grey"


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
canvas = t.Canvas(leftFrame, width = CANVAS_SIZE[0], height = CANVAS_SIZE[1], bg = 'black')
fond = t.PhotoImage(file = "Space2.png")
canvas.create_image(0,0,anchor = "nw", image = fond)
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


options = interract.GameOptions(FRAMERATE,BORDER_PADDING,ALIEN_SPEED,ALIEN_SIZE, ALIEN_Y_MOVE,ENTITIES_TYPES,
 ALIEN_SHOOTING_CHANCE, SHOOTING_ALIEN_PROPORTION, N_ALIEN,SPAWN_PADDING,ALIEN_PADDING,N_WALLS)

gameManager = interract.Game(options, window, canvas, 3, scoreText)


buttonStart.configure(command= gameManager.Restart)

canvas.bind("<<GameStarted>>", lambda event: buttonStart.configure(text="Restart"))   

window.mainloop()