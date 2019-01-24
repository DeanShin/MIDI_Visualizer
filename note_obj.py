# this file holds the NoteObj class

class NoteObj():

    def __init__(self, note_id, channel, velocity, lin_map_vel, spd, is_sustain, width, col1, col2):
        self.note_id = note_id
        self.velocity = velocity
        self.channel = channel
        self.height = 0
        self.width = width
        self.x = note_id * self.width
        self.y = 0
        self.change_y = spd
        #making note color change as velocity 
        #if col1 is yellow (255, 255, 0) and col2 is blue (0, 0, 255)
        #then equation becomes (col1[0] + lin_map_vel * (col2[0] - col1[0]))
        self.color = (int(col1[0] + lin_map_vel * (col2[0] - col1[0])), \
        int(col1[1] + lin_map_vel * (col2[1] - col1[1])), \
        int(col1[2] + lin_map_vel * (col2[2] - col1[2])))
        self.thickness = 2
        self.growing = True
        self.shrinking = False
        self.is_sustain = True
        if is_sustain is True:
            self.x = 0
            self.color = (47, 47, 47)

    def stop_growing(self):
        self.growing = False

    def start_shrinking(self):
        self.shrinking = True

    def move(self):
        if self.growing:
            self.height += self.change_y
        else:
            self.y += self.change_y
            if self.shrinking:
                self.height -= self.change_y

    def draw(self, pygame, window):
        #print("drawing " + str(self.x) + " " + str(self.y))
        #innards
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)
        #shell
        pygame.draw.rect(window, (0, 0, 0), (self.x, self.y, self.width, self.height), self.thickness)
        #if self.is_sustain is True:
        
