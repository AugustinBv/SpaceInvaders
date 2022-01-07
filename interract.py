import tkinter as t
class instance:
    def __init__(self, window,  canevas, position, size, speed, health):
        self.window = window
        self.canevas = canevas
        self.position = position
        self.size = size
        self.speed = speed
        self.health = health
        self.image = self.canevas.create_oval(self.position[0],self.position[1],self.position[0]+self.size,self.position[1]+self.size, fill='red')
    
    
class alien(instance):
    def applySpeed(self):
        self.canevas.move(self.image,self.speed,0)
        self.window.after(10, self.applySpeed)

class player(instance):
    def __init__(self, window, canevas, position, size, speed, health):
        super().__init__(window, canevas, position, size, speed, health)
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
        