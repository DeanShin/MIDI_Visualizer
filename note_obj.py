# this file holds the NoteObj class

class NoteObj():

    def __init__(self, note_id, channel, velocity, lin_map_vel, spd, is_sustain, width, col1, col2, offset):
        self.note_id = note_id
        self.velocity = velocity
        self.channel = channel
        self.height = offset
        self.width = width
        self.x = note_id * self.width
        self.y = 0
        self.change_y = spd
        #making note color change as velocity changes
        self.color = (int(col1[0] + lin_map_vel * (col2[0] - col1[0])), \
        int(col1[1] + lin_map_vel * (col2[1] - col1[1])), \
        int(col1[2] + lin_map_vel * (col2[2] - col1[2])))
        self.thickness = 1
        self.growing = True
        self.shrinking = False
        self.is_sustain = True
        if is_sustain is True:
            self.x = 0
            self.color = (47, 47, 47)
        

    def stop_growing(self, offset):
        self.growing = False
        self.y = self.y - offset

    def start_shrinking(self):
        self.shrinking = True

    def update(self):
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
        pygame.draw.rect(window, (127, 127, 127), (self.x, self.y, self.width, self.height), self.thickness)