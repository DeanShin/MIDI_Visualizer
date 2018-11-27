class Note():
    # this file holds the note class 
    def __init__(channel, note, velocity, time):
        self.height = 30
        self.width = 20
        self.x = note * 20
        self.y = 0
        self.change_x = 0
        self.change_y = 5
        self.color = (0,0,128)
        self.thickness = 1
    def move(self):
        self.x += self.change_x
        self.y += self.change_y
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), self.thickness)
        
        
        
        
    

        
        
