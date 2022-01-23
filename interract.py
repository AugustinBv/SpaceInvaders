from email.mime import image
import tkinter as t
from random import randint

import time
from turtle import pos

def checkForCollision(coordsA, coordsB):
    # Fonction qui indique si les rectangles A et B se chevauchent
    # coordsA et coordsB sont de la forme [x1,y1,x2,y2]
    
    areColliding = False

    if (coordsA[2] >= coordsB[0] and 
        coordsA[0] <= coordsB[2] and 
        coordsA[3] >= coordsB[1] and 
        coordsA[1] <= coordsB[3] ):

        areColliding = True

    return areColliding


class GameOptions :

    # Objet contenant plusieurs informations pour le bon déroulement du jeu

    def __init__(self, frameRate, screenBorderPadding, alienSpeed, alienSize, alienDownMove, entitiesTypes, shootingChance,
     shootingAlienProportion, nAliens, spawnPadding, alienPadding, nWalls):

        self.frameRate = frameRate
        self.frameTime = 1/float(frameRate) * 1000
        self.screenBorderPadding = screenBorderPadding
        self.alienSpeed = alienSpeed
        self.alienSize = alienSize
        self.alienDownMove = alienDownMove
        self.entitiesTypes = entitiesTypes
        self.shootingChance = shootingChance
        self.shootingAlienProportion = shootingAlienProportion

        self.nAliens = nAliens
        self.spawnPadding = spawnPadding
        self.alienPadding = alienPadding
        self.nWalls = nWalls

class Game :

    # Objet maitre qui contient tous les autres objets et qui contient les méthodes principales du jeu, il gère le déroulement de la partie

    def __init__(self,options, master, canvas, lives, text):

        self.options = options
        self.master = master
        self.canvas = canvas
        self.textLabel = text

        self.score = 0
        self.startLives = lives
        self.lives = lives

        self.cheat = [0,0,0,0,0,0,0,0]
        self.canvas.bind('<Key>', self.keys)

        self.currentLevel = None
        self.currentPlayer = None
        self.lost = False
    
    def updateLabel(self):
        # Méthode qui met à jour le texte du label avec le score et les vies restantes
        self.textLabel.set("score : " + str(self.score) + "      vies : " + str(self.lives))       

    def scoreUp(self, value):
        # Méthode qui ajoute le montant "value" au score
        self.score += value
        self.updateLabel()       
    
    def keys(self, event):
        # Méthode qui gère les interractions avec le clavier
        key = event.keysym
        if key == "space":
            self.shoot(self.attackSpeed,self.attackHP,self.attackRange)
        elif key != "Left" and key != "Right":
            self.cheat.remove(self.cheat[0])
            self.cheat.append(key)
            self.cheatCode(self.cheat)
            
    def cheatCode(self, lstcode):
        # Méthode qui applique les cheat codes en lisant la liste des 8 derniers inputs autres que les touches directionnelles
        if lstcode == ["t","u","p","u","d","u","c","u"] :
            self.scoreUp(1000)
        elif lstcode == ["v","i","v","e","l","a","v","i"] :
            self.lives += 3
            self.updateLabel()
        elif lstcode == ["v","a","c","h","i","e","r","m"] :
            while self.currentLevel.entities["alien"] != []:
                self.currentLevel.entities["alien"][0].removeHP(1000)

    def startLevel(self):
        # Méthode qui initialise le niveau en créant les ennemis, le joueur et lance les méthodes récursives

        self.canvas.event_generate("<<GameStarted>>")
        self.levelIsRunning = True
        self.currentLevel = Level(self) # Initialisation du niveau

        self.currentLevel.createAliens(self.options.nAliens, self.options.spawnPadding, self.options.alienPadding) # création des aliens
        self.currentLevel.createWalls(self.options.nWalls)
        self.currentPlayer = player([400,550],20,10,1,self.currentLevel,self.options.entitiesTypes[0], 0.3) # création du joueur

        self.currentLevel.gameLoop() # Lancement des méthodes récursives pour le déplacement des aliens et des lasers 

    
    def Restart(self):
        # Méthode appelé pour lancer le niveau quand on commence ou recommence la partie ou quand on meurt

        if(self.currentLevel != None): # si ce n'est pas la première fois que l'on lance un niveau
            self.currentLevel.gameOver = True
            self.currentLevel.clearLevel() # on supprime les entités du niveau actuel
        
        if(self.lost): # si on vient de mourrir
            self.lives -=1 #on enlève une vie
            self.lost = False
        else:
            self.lives = self.startLives # remise à zéro de la vie et du score
            self.score = 0
        self.updateLabel() #mise à jour du label

        if(not self.lives <=0): # si il nous reste des vies
            self.startLevel() 

        fond = t.PhotoImage(file = "Space2.png")
        self.canvas.create_image(0,0,anchor = "nw", image = fond)
            
    


class Level :

    # Objet contenant tous les entités du jeu et les gèrent

    def __init__(self, game):

        self.game = game
        self.options = self.game.options
        self.canvas = self.game.canvas
        self.master = self.game.master

        self.alienDown = False
        self.alienSpeed = self.options.alienSpeed

        self.entities= {}
        for type in self.options.entitiesTypes :
            self.entities[type] = []
        
        self.gameOver = False
    
    def gameLoop(self):
        # méthode qui lance les méthodes récursives pour le déplacement des aliens et des lasers 
        self.moveAliens()
        self.moveLaser()
        self.entities["player"][0].checkForCollisionWithAliens() # on vérifie que les aliens n'entre pas en collision avec le joueur

    def addEntity(self, entity, type):
        # méthode pour ajouter une nouvelle entité dans le niveau
        self.entities[type].append(entity)
    
    def createWalls(self, nWalls):
        counter = 0
        offset = 50
        wallPad = 50
        while counter < nWalls :
            wall([offset,500], 15, 1, self, self.options.entitiesTypes[2])
            offset += wallPad + 15
            counter += 1
    
    def createAliens(self,n, spawnPadding, alienPadding):
        # méthode qui crée n nombre d'aliens des 2 types (ceux qui tirent et ceux qui ne tirent pas)
        counter = 0
        xOffset = spawnPadding
        yOffset = 20

        while counter < n:
            if( xOffset + alienPadding + self.options.alienSize > self.master.winfo_width() - spawnPadding): # gestion de la position du nouvel alien
                xOffset = spawnPadding
                yOffset += 20
            if(randint(1,1000) < 1000 * self.options.shootingAlienProportion): # choix de création d'un type d'alien selon la proportion voulue
                shootingAlien([xOffset,yOffset], self.options.alienSize, 1, self, self.options.entitiesTypes[1],25)
            else:
                alien([xOffset,yOffset], self.options.alienSize, 1, self, self.options.entitiesTypes[1],10)
            xOffset += alienPadding + self.options.alienSize # on se décale
            counter += 1

    def changeAlienDir(self):
        # méthode qui permet de changer la direction de déplacement des aliens (gauche /droite) et vérifie si ils ont fait un aller-retour
        self.alienSpeed *= -1
        if(self.alienSpeed > 0): # si les aliens se déplacent de nouveau vers la droite, c'est qu'ils on fait un aller retour
            self.alienDown = True # On envoi donc le signal pour qu'ils descendent d'une ligne
    
    def moveLaser(self):
        # méthode qui déplacent les lasers 
        if(not self.gameOver):
            for laser in self.entities["laser"]:
                laser.laserShot()
            self.master.after(int(self.options.frameTime), self.moveLaser) # on rappelle la frame après le temps d'une frame
    
    def moveAliens(self):
        # méthode qui déplacent les aliens
        if(not self.gameOver):

            if(randint(1,1000) < 1):
                bonusAlien([-100,self.entities["alien"][1].getPos()[1] - 50], self.options.alienSize, 1, self, self.options.entitiesTypes[1],150)

            for alien in self.entities["alien"]: # On vérifie si un des aliens touche le bord
                alien.checkForBorders()
            for alien in self.entities["alien"]:
                if(self.alienDown): 
                    alien.moveDown() # on fait descendre chaque alien si le signal est actif
                alien.move() # on déplace chaque alien
            self.alienDown = False # on désactive le signal
        
            self.master.after(int(self.options.frameTime), self.moveAliens) # on rappelle la frame après le temps d'une frame

    def clearLevel(self):
        # méthode qui retire toutes les entités
        self.canvas.delete('all') # on retire toutes les images du canvas
        self.entities.clear() # on vide le dictionnaire des entités
        
            
            

class instance:

    # Objet dont hérite chaque élément qui peut intéragir avec les autres (joueur, aliens, etc)

    def __init__(self, position, size, health, level, type, image):
        self.position = position
        self.size = size
        self.health = health

        self.level = level

        self.canvas = self.level.canvas

        self.type = type
        self.level.addEntity(self,self.type)
        
        self.image = image

        if(self.image == None):
            self.image = self.canvas.create_oval(self.position[0],self.position[1],self.position[0]+ self.size,self.position[1]+self.size, fill='red')
        else:
            self.image = self.canvas.create_image(self.position[0],self.position[1], anchor = "nw", image = self.image)

        
    def removeHP(self, value):
        # Méthode qui permet de retirer des points de vie et gérer la "mort" de l'objet
        self.health -= value
        if self.health<=0 :
            self.health = 0
            self.level.entities[self.type].remove(self)
            self.canvas.delete(self.image)
    




class alien(instance):
    
    # Objet de base pour les ennemis

    def __init__(self, position, size, health, level, type, value,image = None):
        super().__init__(position, size, health, level, type, image)
        
        self.canvas.itemconfig(self.image, fill = 'green')
        self.value = value

    def getPos(self):
        # Méthode qui retourne la position de l'objet
        return self.canvas.coords(self.image)[:2]

    def move(self):
        # Méthode qui permet de déplacer l'objet
        self.canvas.move(self.image,self.level.alienSpeed,0)
        self.position = self.canvas.coords(self.image)
    
    def checkForBorders(self):
        # Méthode utilisée pour vérifier les collisions avec les bords
        newX = self.getPos()[0] + self.level.alienSpeed
        if self.level.options.screenBorderPadding > newX or newX > (self.canvas.winfo_width() - self.level.options.screenBorderPadding - self.size) :
            self.level.changeAlienDir()
    
    def moveDown(self):
        # Méthode qui permet aux aliens de descendre d'une ligne
        self.canvas.move(self.image, 0, self.level.options.alienDownMove)



class shootingAlien(alien):

    # Objet ennemi qui peut tirer, hérite d'alien

    def __init__(self, position, size, health, level, type, value,image = None):
        super().__init__(position, size, health, level, type, value,image)  
        self.canvas.itemconfig(self.image, fill = 'yellow')

    def move(self):
        # Méthode qui s'occupe du déplacement et permet à l'objet de tirer avec une certaine probabilité
        super().move()
        if randint(1,1000) < self.level.options.shootingChance * 1000 :
            tir = laser(self.position, 1, self.level, "laser", 10, 5, 1)    

class bonusAlien(alien):

    def __init__(self, position, size, health, level, type, value, image=None):
        super().__init__(position, size, health, level, type, value, image)
        self.canvas.itemconfig(self.image, fill = 'purple')
    
    def move(self):
        # Méthode qui permet de déplacer l'objet
        self.canvas.move(self.image,self.level.alienSpeed * self.level.alienSpeed,0)
        self.position = self.canvas.coords(self.image)

    def moveDown(self):
        return None

    def checkForBorders(self):
        # Méthode utilisée pour vérifier les collisions avec les bords
        if self.getPos()[0] > self.canvas.winfo_width() +200:
            self.canvas.delete(self.image)
            self.level.entities[self.type].remove(self)


class player(instance):

    # Objet joueur

    def __init__(self, position, size, speed, health,level, type, shootDelay,image = None):
        super().__init__(position, size, health,level, type,image)

        self.speed = speed
        self.attackSpeed = 30
        self.attackRange = 5
        self.attackHP = 1

        self.lastShot = time.time()
        self.shootDelay = shootDelay

        self.canvas.bind('<Right>', self.move)
        self.canvas.bind('<Left>', self.move)
        self.canvas.bind('<space>', lambda event : self.shoot(2,1,15,event))
    
    def move(self, event):
        # Méthode pour le déplacement du joueur, s'occupe également de la collision avec les bords
        if(not self.level.gameOver):
            dir = 1
            if event.keysym == "Left":
                dir = -1

            moveX = self.speed*dir
            newX = self.position[0] + moveX
            if not(self.level.options.screenBorderPadding > newX or newX > (self.canvas.winfo_width() - self.level.options.screenBorderPadding - self.size)) :
                self.canvas.move(self.image,self.speed*dir,0)
                self.position = self.canvas.coords(self.image)[:2]

            
    def shoot(self, speed, hp, size, event):
        # Méthode qui permet au joueur de tirer un laser
        if(not self.level.gameOver):
            currentTime = time.time()
            if((currentTime - self.lastShot) > self.shootDelay):
                tir = laser([self.position[0],self.position[1] - 30], -1, self.level,"laser", size, speed, hp)
                self.lastShot = time.time()

    def removeHP(self, value):
        # Méthode qui gère les points de vie du joueur et permet de dire si la partie est perdue
        super().removeHP(value)
        if(self.health <=0):
            self.level.game.lost = True
            self.level.game.Restart()

    def checkForCollisionWithAliens(self):
        # Méthode qui vérifie la collision avec les ennemis et fait perdre le joueur
        if(not self.level.gameOver):
            for alien in self.level.entities["alien"]:
                if type(alien) != bonusAlien :
                    if(checkForCollision(self.canvas.coords(self.image),self.canvas.coords(alien.image))):
                        self.removeHP(1)
            self.level.master.after(int(self.level.options.frameTime), self.checkForCollisionWithAliens)
            

class wall(instance):

    def __init__(self, position, size, health, level, type):
        super().__init__(position, size, health, level, type)
        self.image = self.canvas.create_rectangle(self.position[0],self.position[1],self.position[0]+ self.size,self.position[1]+self.size, fill='blue')


class laser(instance):

    # Objet laser tiré par le joueur ou les aliens

    def __init__(self, position, direction, level, type, size, speed, health, image = None) :
        super().__init__(position, size, health, level,type,image)
        self.speed = speed
        self.direction = direction
        self.canvas.itemconfig(self.image, fill = 'yellow')
        
    def laserShot(self):
        # Méthode qui s'occupe du déplacement et des collisions du laser
        if(not self.level.gameOver):
            moveY = self.speed*self.direction
            newY = self.position[1] + moveY
            if self.level.options.screenBorderPadding > newY or newY > (self.canvas.winfo_height() - self.level.options.screenBorderPadding - self.size) :
                self.removeHP(self.health)
            elif self.direction == -1 :
                for alien in self.level.entities["alien"] :
                    if(checkForCollision(self.canvas.coords(self.image),self.canvas.coords(alien.image))):
                        alien.removeHP(self.health)
                        self.removeHP(self.health)
                        self.level.game.scoreUp(alien.value)
                        break
            else :
                for entity in self.level.entities["player"] + self.level.entities["wall"] :
                    if(checkForCollision(self.level.canvas.coords(self.image), self.canvas.coords(entity.image))):
                        attack = self.health
                        self.removeHP(self.health)
                        entity.removeHP(attack)
            self.canvas.move(self.image, 0, moveY)
            self.position = self.canvas.coords(self.image)[:2]