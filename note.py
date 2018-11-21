class Note():
    # this file holds the note class 
    def __init__(channel, note, velocity, time):
        self.height = 30
        self.width = 20

        self.x = 20
        self.y = 20

        self.change_x = 0
        self.change_y = 5
    def move(self):
        self.x += self.change_x
        self.y += self.change_y
    def draw(self):
        #draw note
        pass
        
        
        
    

        
        
