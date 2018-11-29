class NoteObj():
    # this file holds the note class 
    def __init__(self, x, channel, velocity):
        self.height = 5
        self.width = 20 
        self.x = x * 20
        self.y = 0
        self.change_x = 0
        self.change_y = 5
        self.color = (0,0,128)
        self.thickness = 1
        self.is_still_on = true
        
    def stop_growing(self):
        self.is_still_on = false
        
    def move(self):
        self.x += self.change_x
        
        if self.is_still_on:
            self.height += self.change_y
        else: 
            self.y += self.change_y
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), self.thickness)
       
