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
        
        