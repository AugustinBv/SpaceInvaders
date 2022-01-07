class interact:
    def __init__(self, position, size, speed, health):
        self.position = position
        self.size = size
        self.speed = speed
        self.health = health
    
    
class alien(interact):
    def move(self):
        self.position += self.speed
        