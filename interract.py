class instance:
    def __init__(self, canevas, position, size, speed, health):
        self.canevas = canevas
        self.position = position
        self.size = size
        self.speed = speed
        self.health = health
    
    
class alien(instance):
    def move(self):
        self.position[0] += self.speed
        self.canevas.coords(self, self.position[0],self.position[1],self.position[0]+self.size,self.position[1]+self.size)
        self.canevas.after(20,alien.move(self))
        