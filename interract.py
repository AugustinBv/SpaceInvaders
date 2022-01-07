import tkinter as t


def checkForCollision(coordsA, coordsB):
    
    colliding = False

    if (coordsA[2] >= coordsB[0] and 
        coordsA[0] <= coordsB[2] and 
        coordsA[3] >= coordsB[1] and 
        coordsA[1] <= coordsB[3] ):

        colliding = True
    return colliding

    

class ennemies :

    def __init__(self, window, frameRate, borderPadding, speed, yOffset):

        self.window = window

        self.delta = 1/float(frameRate) * 1000
        self.borderPadding = borderPadding
        self.speed = speed

        self.down = False
        self.yOffset = yOffset

        self.listAliens = []
    
    def addAlien(self, alien):
        self.listAliens.append(alien)
    
    def changeDir(self):
        self.speed *= -1
        if(self.speed > 0):
            self.down = True
            
    
    def moveAliens(self):
        for alien in self.listAliens:
            alien.checkForBorders()
        for alien in self.listAliens:
            if(self.down):
                alien.goDown()
            alien.applySpeed()
        self.down = False
        self.window.after(int(self.delta), self.moveAliens)
            
            


class instance:
    def __init__(self, canevas, position, size, health):

        self.canevas = canevas
        self.position = position
        self.size = size
        self.health = health
        
        self.image = self.canevas.create_oval(self.position[0],self.position[1],self.position[0]+self.size,self.position[1]+self.size, fill='red')
    
    
class alien(instance):
    
    def __init__(self, canevas, position, size, health, group):

        super().__init__(canevas, position, size, health)
        self.group = group
        self.group.addAlien(self)

    def getPos(self):
        return self.canevas.coords(self.image)[:1]

    def applySpeed(self):
        self.canevas.move(self.image,self.group.speed,0)
    
    def checkForBorders(self):
        newX = self.getPos()[0] + self.group.speed
        if self.group.borderPadding > newX or newX > (self.canevas.winfo_width() - self.group.borderPadding - self.size) :
            self.group.changeDir()
    
    def goDown(self):
        self.canevas.move(self.image, 0, self.group.yOffset)


        

class player(instance):
    def __init__(self, canevas, position, size, speed, health):
        super().__init__(canevas, position, size, health)
        self.speed = speed
        self.cheat = [0,0,0,0,0,0,0,0]
        self.attackSpeed = 30
        self.attackRange = 5
        self.attackHP = 1
    
    def bougeSTP(self, event):
        dir = 1
        if event.keysym == "Left":
            dir = -1
        self.canevas.move(self.image,self.speed*dir,0)
        self.position = self.canevas.coords(self.image)[:1]
    
    def keys(self, event):
        key = event.keysym
        print(type(self.cheat))
        if key == "space":
            self.shoot(self.attackSpeed,self.attackHP,self.attackRange)
        elif key != "Left" and key != "Right":
            self.cheat.remove(self.cheat[0])
            self.cheat.append(key)
            print(self.cheat)
            
    def shoot(self, speed, hp, size):
         print("pute")
            
        
class laser(instance):
    def __init__(self, window, canevas, position, size = 5, speed = 30, health = 1):
        super().__init__(window, canevas, position, size, speed, health)
        