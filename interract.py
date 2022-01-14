import tkinter as t


def checkForCollision(coordsA, coordsB):
    
    colliding = False

    if (coordsA[2] >= coordsB[0] and 
        coordsA[0] <= coordsB[2] and 
        coordsA[3] >= coordsB[1] and 
        coordsA[1] <= coordsB[3] ):

        colliding = True
    return colliding

def updateScore(scoreLabel):
    scoreLabel.config()


class entities :

    def __init__(self, window, frameRate, borderPadding, speed, yOffset):

        self.window = window

        self.delta = 1/float(frameRate) * 1000
        self.borderPadding = borderPadding
        self.speed = speed

        self.down = False
        self.yOffset = yOffset

        self.listEntities= [[], [], [], []]
    
    def addEntity(self, entity, type = 1):
        self.listEntities[type].append(entity)
    
    def changeDir(self):
        self.speed *= -1
        if(self.speed > 0):
            self.down = True
    
    def moveLaser(self):
        for laser in self.listEntities[3]:
            
        self.window.after(int(self.delta), self.moveLaser())
    
    def moveAliens(self):
        for alien in self.listEntities[1]:
            alien.checkForBorders()
        for alien in self.listEntities[1]:
            if(self.down):
                alien.goDown()
            alien.applySpeed()
        self.down = False
        self.window.after(int(self.delta), self.moveAliens)
            
            


class instance:
    def __init__(self, canevas, position, size, health, entities):

        self.canevas = canevas
        self.position = position
        self.size = size
        self.health = health
        self.entities = entities
        
        self.image = self.canevas.create_oval(self.position[0],self.position[1],self.position[0]+self.size,self.position[1]+self.size, fill='red')
        
    def removeHP(self, value):
        self.health -= value
        if self.health<=0 :
            self.entities.listEntities[1].remove(self)
            self.destroy()
    
class alien(instance):
    
    def __init__(self, canevas, position, size, health, entities):

        super().__init__(canevas, position, size, health, entities)
        self.entities.addEntity(self,1)

    def getPos(self):
        return self.canevas.coords(self.image)[:1]

    def applySpeed(self):
        self.canevas.move(self.image,self.entities.speed,0)
    
    def checkForBorders(self):
        newX = self.getPos()[0] + self.entities.speed
        if self.entities.borderPadding > newX or newX > (self.canevas.winfo_width() - self.entities.borderPadding - self.size) :
            self.entities.changeDir()
    
    def goDown(self):
        self.canevas.move(self.image, 0, self.entities.yOffset)

    

        

class player(instance):
    def __init__(self, canevas, position, size, speed, health,entities):
        super().__init__(canevas, position, size, health,entities)
        self.speed = speed
        self.cheat = [0,0,0,0,0,0,0,0]
        self.attackSpeed = 30
        self.attackRange = 5
        self.attackPower = 1
        self.score = 0
        self.entities.addEntity(self,0)
    
    def bougeSTP(self, event):
        dir = 1
        if event.keysym == "Left":
            dir = -1
        self.canevas.move(self.image,self.speed*dir,0)
        self.position = self.canevas.coords(self.image)[:1]

    def keys(self, event):
        key = event.keysym
        if key == "space":
            self.shoot(self.attackSpeed,self.attackHP,self.attackRange)
        elif key != "Left" and key != "Right":
            self.cheat.remove(self.cheat[0])
            self.cheat.append(key)
            self.cheatCode(self.cheat)
            
    def shoot(self, speed, hp, size):
        tir = laser(self.canevas, self.position, 1, self.entities size, speed, hp)

    def getScore(self):
        print(self.score)
        return self.score
    
    def getHealth(self):
        return self.health

    def cheatCode(self, lstcode):
        if lstcode == ["t","u","p","u","d","u","c","u"] :
            self.scoreUp(1000)
        if lstcode == ["v","i","v","e","l","a","v","i"] :
            self.health += 3
            print(self.health)

    def scoreUp(self, value):
        self.score += value
        print(self.score)

    
    def checkForCollisionWithAliens(self):
        for alien in self.entities.listEntities[1]:
            if(checkForCollision(self.canevas.coords(self.image),self.canevas.coords(alien.image))):
                print("touché")
        self.entities.window.after(int(self.entities.delta), self.checkForCollisionWithAliens)
            
        
class laser(instance):
    def __init__(self, canevas, position, direction, entities, size = 5, speed = 10, health = 1):
        super().__init__(canevas, position, size, speed, health, entities)
        self.direction = direction
        
     def getPos(self):
        return self.canevas.coords(self.image)[:1]
        
    def laserShot(self):
        newY = self.getPos()[0] + self.speed*self.direction
        if self.entities.borderPadding > newY or newY > (self.canevas.winfo_height() - self.entities.borderPadding - self.size) :
            self.entities[3].remove(self)
            self.destroy()
        if self.direction == 1 :
            for alien in self.entities.listEntities[1] :
                if(checkForCollision(self.canevas.coords(self.image),self.canevas.coords(alien.image))):
                    self.entities.listEntities[3].remove(self)
                    alien.removeHP(self.health)
                    break
        for typeEntities in self.entities :
            for entity in typeEntities :
                checkForCollision(self.canevas.coords(self.image), coordsB)
            
        