import tkinter as t
from random import randint

import time

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

    def __init__(self, frameRate, screenBorderPadding, alienSpeed, alienSize, alienDownMove, entitiesTypes, shootingChance, shootingAlienProportion):
        self.frameRate = frameRate
        self.frameTime = 1/float(frameRate) * 1000
        self.screenBorderPadding = screenBorderPadding
        self.alienSpeed = alienSpeed
        self.alienSize = alienSize
        self.alienDownMove = alienDownMove
        self.entitiesTypes = entitiesTypes
        self.shootingChance = shootingChance
        self.shootingAlienProportion = shootingAlienProportion

class Game :

    def __init__(self,gameOptions, master, canvas, lives, text):

        self.gameOptions = gameOptions
        self.master = master
        self.canvas = canvas
        self.textLabel = text

        self.score = 0
        self.lives = lives

        self.cheat = [0,0,0,0,0,0,0,0]
        self.canvas.bind('<Key>', self.keys)

        self.currentLevel = None
        self.currentPlayer = None

        self.levelIsRunning = False
    
    def updateLabel(self):
        self.textLabel.set("score : " + str(self.score) + "      vies : " + str(self.lives))       

    def scoreUp(self, value):
        self.score += value
        self.updateLabel()       
    
    def keys(self, event):
        key = event.keysym
        if key == "space":
            self.shoot(self.attackSpeed,self.attackHP,self.attackRange)
        elif key != "Left" and key != "Right":
            self.cheat.remove(self.cheat[0])
            self.cheat.append(key)
            self.cheatCode(self.cheat)
            
    def cheatCode(self, lstcode):
        if lstcode == ["t","u","p","u","d","u","c","u"] :
            self.scoreUp(1000)
        elif lstcode == ["v","i","v","e","l","a","v","i"] :
            self.lives += 3
        elif lstcode == ["v","a","c","h","i","e","r","m"] :
            while self.currentLevel.entities["alien"] != []:
                self.currentLevel.entities["alien"][0].removeHP(1000)

    def startLevel(self,nAlien, spawnPadding, alienPadding):

        if(not self.levelIsRunning):
            self.levelIsRunning = True
            self.currentLevel = Level(self)
            self.currentLevel.createAliens(nAlien, spawnPadding, alienPadding)
            self.currentPlayer = player([400,550],20,10,1,self.currentLevel,self.gameOptions.entitiesTypes[0], 0.3)
            self.currentLevel.gameLoop()
    
    def gameOver(self):

        self.currentLevel.gameOver = True

        self.lives -= 1
        self.updateLabel()

        self.currentLevel.clearLevel()

        self.levelIsRunning = False


class Level :

    def __init__(self, game):

        self.game = game
        self.gameOptions = self.game.gameOptions
        self.canvas = self.game.canvas
        self.master = self.game.master

        self.alienDown = False
        self.alienSpeed = self.gameOptions.alienSpeed

        self.entities= {}
        for type in self.gameOptions.entitiesTypes :
            self.entities[type] = []
        
        self.gameOver = False
    
    def gameLoop(self):
        self.moveAliens()
        self.moveLaser()
        self.entities["player"][0].checkForCollisionWithAliens()

    def addEntity(self, entity, type):
        self.entities[type].append(entity)
    
    def createAliens(self,n, spawnPadding, alienPadding):
        counter = 0
        xOffset = spawnPadding
        yOffset = 20

        while counter < n:
            if( xOffset + alienPadding + self.gameOptions.alienSize > 800 - spawnPadding):
                xOffset = spawnPadding
                yOffset += 20
            if(randint(1,1000) < 1000 * self.gameOptions.shootingAlienProportion):
                shootingAlien([xOffset,yOffset], self.gameOptions.alienSize, 1, self, self.gameOptions.entitiesTypes[1])
            else:
                alien([xOffset,yOffset], self.gameOptions.alienSize, 1, self, self.gameOptions.entitiesTypes[1])
            xOffset += alienPadding + self.gameOptions.alienSize
            counter += 1

    def changeAlienDir(self):
        self.alienSpeed *= -1
        if(self.alienSpeed > 0):
            self.alienDown = True
    
    def moveLaser(self):
        if(not self.gameOver):
            for laser in self.entities["laser"]:
                laser.laserShot()
            self.master.after(int(self.gameOptions.frameTime), self.moveLaser)
    
    def moveAliens(self):
        if(not self.gameOver):
            for alien in self.entities["alien"]: 
                alien.checkForBorders()
            for alien in self.entities["alien"]:
                if(self.alienDown):
                    alien.moveDown()
                alien.move()
            self.alienDown = False
        
            self.master.after(int(self.gameOptions.frameTime), self.moveAliens)

    def clearLevel(self):
        self.canvas.delete('all')
        self.entities.clear()
            
            

class instance:
    def __init__(self, position, size, health, level, type):
        self.position = position
        self.size = size
        self.health = health

        self.level = level

        self.canvas = self.level.canvas

        self.type = type
        self.level.addEntity(self,self.type)
        
        self.image = self.canvas.create_oval(self.position[0],self.position[1],self.position[0]+ self.size,self.position[1]+self.size, fill='red')
        
    def removeHP(self, value):
        self.health -= value
        if self.health<=0 :
            self.health = 0
            self.level.entities[self.type].remove(self)
            self.canvas.delete(self.image)
    


class alien(instance):
    
    def __init__(self, position, size, health, level, type):
        super().__init__(position, size, health, level, type)
        self.canvas.itemconfig(self.image, fill = 'green')

    def getPos(self):
        return self.canvas.coords(self.image)[:1]

    def move(self):
        self.canvas.move(self.image,self.level.alienSpeed,0)
        self.position = self.canvas.coords(self.image)
    
    def checkForBorders(self):
        newX = self.getPos()[0] + self.level.alienSpeed
        if self.level.gameOptions.screenBorderPadding > newX or newX > (self.canvas.winfo_width() - self.level.gameOptions.screenBorderPadding - self.size) :
            self.level.changeAlienDir()
    
    def moveDown(self):
        self.canvas.move(self.image, 0, self.level.gameOptions.alienDownMove)

class shootingAlien(alien):

    def __init__(self, position, size, health, level, type):
        super().__init__(position, size, health, level, type)  
        self.canvas.itemconfig(self.image, fill = 'yellow')

    def move(self):
        super().move()
        if randint(1,1000) < self.level.gameOptions.shootingChance * 1000 :
            tir = laser(self.position, 1, self.level, "laser", 10, 5, 1)    

class player(instance):
    def __init__(self, position, size, speed, health,level, type, shootDelay):
        super().__init__(position, size, health,level, type)

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
        dir = 1
        if event.keysym == "Left":
            dir = -1

        moveX = self.speed*dir
        newX = self.position[0] + moveX
        if not(self.level.gameOptions.screenBorderPadding > newX or newX > (self.canvas.winfo_height() - self.level.gameOptions.screenBorderPadding - self.size)) :
            self.canvas.move(self.image,self.speed*dir,0)
            self.position = self.canvas.coords(self.image)[:2]

            
    def shoot(self, speed, hp, size, event):
        currentTime = time.time()
        if((currentTime - self.lastShot) > self.shootDelay):
            tir = laser([self.position[0],self.position[1] - 30], -1, self.level,"laser", size, speed, hp)
            self.lastShot = time.time()

    def removeHP(self, value):
        super().removeHP(value)
        if(self.health <=0):
            self.level.game.gameOver()

    def checkForCollisionWithAliens(self):
        if(not self.level.gameOver):
            for alien in self.level.entities["alien"]:
                if(checkForCollision(self.canvas.coords(self.image),self.canvas.coords(alien.image))):
                    self.removeHP(1)
            self.level.master.after(int(self.level.gameOptions.frameTime), self.checkForCollisionWithAliens)
            
        

class laser(instance):

    def __init__(self, position, direction, level, type, size = 5, speed = 10, health = 1) :
        super().__init__(position, size, health, level,type)
        self.speed = speed
        self.direction = direction
        self.canvas.itemconfig(self.image, fill = 'yellow')
        
    def laserShot(self):
        if(not self.level.gameOver):
            moveY = self.speed*self.direction
            newY = self.position[1] + moveY
            if self.level.gameOptions.screenBorderPadding > newY or newY > (self.canvas.winfo_height() - self.level.gameOptions.screenBorderPadding - self.size) :
                self.removeHP(self.health)
            elif self.direction == -1 :
                for alien in self.level.entities["alien"] :
                    if(checkForCollision(self.canvas.coords(self.image),self.canvas.coords(alien.image))):
                        alien.removeHP(self.health)
                        self.removeHP(self.health)
                        self.level.game.scoreUp(50)
                        break
            else :
                for entity in self.level.entities["player"] + self.level.entities["wall"] :
                    if(checkForCollision(self.level.canvas.coords(self.image), self.canvas.coords(entity.image))):
                        attack = self.health
                        self.removeHP(self.health)
                        entity.removeHP(attack)
            self.canvas.move(self.image, 0, moveY)
            self.position = self.canvas.coords(self.image)[:2]