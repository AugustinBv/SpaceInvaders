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

    def __init__(self, frameRate, screenBorderPadding, alienSpeed, alienSize, alienDownMove, entitiesTypes, shootingChance,
     shootingAlienProportion, nAliens, spawnPadding, alienPadding):
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

class Game :

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

    def startLevel(self):
        self.canvas.event_generate("<<GameStarted>>")
        self.levelIsRunning = True
        self.currentLevel = Level(self)
        self.currentLevel.createAliens(self.options.nAliens, self.options.spawnPadding, self.options.alienPadding)
        self.currentPlayer = player([400,550],20,10,1,self.currentLevel,self.options.entitiesTypes[0], 0.3)
        self.currentLevel.gameLoop()

    
    def Restart(self):

        if(self.currentLevel != None):
            self.currentLevel.gameOver = True
            self.currentLevel.clearLevel()
        
        if(self.lost):
            self.lives -=1
            self.lost = False
        else:
            self.lives = self.startLives
            self.score = 0

        self.updateLabel()

        if(not self.lives <=0):
            self.startLevel()
            
    


class Level :

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
            if( xOffset + alienPadding + self.options.alienSize > 800 - spawnPadding):
                xOffset = spawnPadding
                yOffset += 20
            if(randint(1,1000) < 1000 * self.options.shootingAlienProportion):
                shootingAlien([xOffset,yOffset], self.options.alienSize, 1, self, self.options.entitiesTypes[1],25)
            else:
                alien([xOffset,yOffset], self.options.alienSize, 1, self, self.options.entitiesTypes[1],10)
            xOffset += alienPadding + self.options.alienSize
            counter += 1

    def changeAlienDir(self):
        self.alienSpeed *= -1
        if(self.alienSpeed > 0):
            self.alienDown = True
    
    def moveLaser(self):
        if(not self.gameOver):
            for laser in self.entities["laser"]:
                laser.laserShot()
            self.master.after(int(self.options.frameTime), self.moveLaser)
    
    def moveAliens(self):
        if(not self.gameOver):
            for alien in self.entities["alien"]: 
                alien.checkForBorders()
            for alien in self.entities["alien"]:
                if(self.alienDown):
                    alien.moveDown()
                alien.move()
            self.alienDown = False
        
            self.master.after(int(self.options.frameTime), self.moveAliens)

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
    
    def __init__(self, position, size, health, level, type, value):
        super().__init__(position, size, health, level, type)
        self.canvas.itemconfig(self.image, fill = 'green')
        self.value = value

    def getPos(self):
        return self.canvas.coords(self.image)[:1]

    def move(self):
        self.canvas.move(self.image,self.level.alienSpeed,0)
        self.position = self.canvas.coords(self.image)
    
    def checkForBorders(self):
        newX = self.getPos()[0] + self.level.alienSpeed
        if self.level.options.screenBorderPadding > newX or newX > (self.canvas.winfo_width() - self.level.options.screenBorderPadding - self.size) :
            self.level.changeAlienDir()
    
    def moveDown(self):
        self.canvas.move(self.image, 0, self.level.options.alienDownMove)



class shootingAlien(alien):

    def __init__(self, position, size, health, level, type, value):
        super().__init__(position, size, health, level, type, value)  
        self.canvas.itemconfig(self.image, fill = 'yellow')

    def move(self):
        super().move()
        if randint(1,1000) < self.level.options.shootingChance * 1000 :
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
        if(not self.level.gameOver):
            currentTime = time.time()
            if((currentTime - self.lastShot) > self.shootDelay):
                tir = laser([self.position[0],self.position[1] - 30], -1, self.level,"laser", size, speed, hp)
                self.lastShot = time.time()

    def removeHP(self, value):
        super().removeHP(value)
        if(self.health <=0):
            self.level.game.lost = True
            self.level.game.Restart()

    def checkForCollisionWithAliens(self):
        if(not self.level.gameOver):
            for alien in self.level.entities["alien"]:
                if(checkForCollision(self.canvas.coords(self.image),self.canvas.coords(alien.image))):
                    self.removeHP(1)
            self.level.master.after(int(self.level.options.frameTime), self.checkForCollisionWithAliens)
            




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