# this file holds the NoteObj class

class NoteObj():

    def __init__(self, note_id, channel, velocity, lin_map_vel, spd, is_sustain):
        self.note_id = note_id
        self.velocity = velocity
        self.channel = channel
        self.height = 0
        self.width = 20
        self.x = note_id * 20
        self.y = 0
        self.change_y = spd
        #making note color change as velocity increases
        self.color = (255, lin_map_vel, 255 - lin_map_vel)
        self.thickness = 2
        self.growing = True
        self.shrinking = False
        self.is_sustain = True
        if is_sustain is True:
            self.width = 1760
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

    def draw(self, pygame, surface):
        #print("drawing " + str(self.x) + " " + str(self.y))
        #innards
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)
        #shell
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height), self.thickness)
        #if self.is_sustain is True:
        
