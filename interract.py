import tkinter as t


def checkForCollision(coordsA, coordsB):
    
    colliding = False

    if (coordsA[2] >= coordsB[0] and 
        coordsA[0] <= coordsB[2] and 
        coordsA[3] >= coordsB[1] and 
        coordsA[1] <= coordsB[3] ):

        colliding = True
    return colliding



class entities :

    def __init__(self, window, frameRate, borderPadding, speed, yOffset, types):

        self.window = window

        self.delta = 1/float(frameRate) * 1000
        self.borderPadding = borderPadding
        self.speed = speed

        self.down = False
        self.yOffset = yOffset

        self.entitiesCodex= {}

        for type in types :
            self.entitiesCodex[type] = []
    
    def addEntity(self, entity, type):
        self.entitiesCodex[type].append(entity)
    
    def changeDir(self):
        self.speed *= -1
        if(self.speed > 0):
            self.down = True
    
    def moveLaser(self):
        for laser in self.entitiesCodex["laser"]:
            laser.laserShot()
        self.window.after(int(self.delta), self.moveLaser)
    
    def moveAliens(self):
        for alien in self.entitiesCodex["alien"]:
            alien.checkForBorders()
        for alien in self.entitiesCodex["alien"]:
            if(self.down):
                alien.goDown()
            alien.applySpeed()
        self.down = False
        self.window.after(int(self.delta), self.moveAliens)

    def clear(self):
        self.entitiesCodex["alien"][0].canevas.delete('all')
            
            


class instance:
    def __init__(self, canevas, position, size, health, entities, type):

        self.canevas = canevas
        self.position = position
        self.size = size
        self.health = health

        self.entities = entities
        self.type = type
        self.entities.addEntity(self,self.type)
        
        self.image = self.canevas.create_oval(self.position[0],self.position[1],self.position[0]+self.size,self.position[1]+self.size, fill='red')
        
    def removeHP(self, value):
        self.health -= value
        if self.health<=0 :
            self.entities.entitiesCodex[self.type].remove(self)
            self.canevas.delete(self.image)
    
class alien(instance):
    
    def __init__(self, canevas, position, size, health, entities, type):

        super().__init__(canevas, position, size, health, entities, type)
        

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
    def __init__(self, canevas, position, size, speed, health,entities, scoreStringVar, type):
        super().__init__(canevas, position, size, health,entities, type)
        self.speed = speed
        self.cheat = [0,0,0,0,0,0,0,0]
        self.attackSpeed = 30
        self.attackRange = 5
        self.attackHP = 1
        self.score = 0
        self.scoreStringVar = scoreStringVar
        self.scoreStringVar.set(str(self.score))

        self.scoreUp(0)
    
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
            
    def shoot(self, speed, hp, size, event):
        tir = laser(self.canevas, self.position, 1, self.entities, size, speed, hp)

    def getScore(self):
        print(self.score)
        return self.score
    
    def getHealth(self):
        return self.health

    def cheatCode(self, lstcode):
        if lstcode == ["t","u","p","u","d","u","c","u"] :
            self.scoreUp(1000)
        elif lstcode == ["v","i","v","e","l","a","v","i"] :
            self.removeHP(-3)
            print(self.health)
        elif lstcode == ["v","a","c","h","i","e","r","m"] :
            while self.entities.entitiesCodex["alien"] != []:
                self.entities.entitiesCodex["alien"][0].removeHP(1000)

            

    def scoreUp(self, value):
        self.score += value
        self.scoreStringVar.set("score : " + str(self.score) + "      vies : " + str(self.health))

    def removeHP(self, value):
        super().removeHP(value)
        self.scoreStringVar.set("score : " + str(self.score) + "      vies : " + str(self.health))

    
    def checkForCollisionWithAliens(self):
        for alien in self.entities.entitiesCodex["alien"]:
            if(checkForCollision(self.canevas.coords(self.image),self.canevas.coords(alien.image))):
                self.removeHP(1)
        self.entities.window.after(int(self.entities.delta), self.checkForCollisionWithAliens)
            
        
class laser(instance):
    def __init__(self, canevas, position, direction, entities, type, size = 5, speed = 10, health = 1) :
        super().__init__(canevas, position, size, health, entities,type)
        self.speed = speed
        self.direction = direction
        
    def getPos(self):
        return self.canevas.coords(self.image)[:1]
        
    def laserShot(self):
        moveY = -self.speed*self.direction
        newY = self.getPos()[0] + moveY
        if self.entities.borderPadding > newY or newY > (self.canevas.winfo_height() - self.entities.borderPadding - self.size) :
            self.entities[3].remove(self)
            self.destroy()
        if self.direction == 1 :
            for alien in self.entities.entitiesCodex["alien"] :
                if(checkForCollision(self.canevas.coords(self.image),self.canevas.coords(alien.image))):
                    self.entities.entitiesCodex[self.type].remove(self)
                    alien.removeHP(self.health)
                    break
        else :
            for typeEntities in self.entities.entitiesCodex["player"] + self.entities.entitiesCodex["wall"] :
                for entity in typeEntities :
                    if(checkForCollision(self.canevas.coords(self.image), self.canevas.coords(entity.image))):
                        self.entities.entitiesCodex[self.type].remove(self)
                        entity.removeHP(self.health)
        self.canevas.move(self.image, 0, moveY)