# this file holds the PianoRollObj class

class PianoRollObj():

    def __init__(self, x, number, screen_y):
        self.is_white_note = False
        self.width = 20
        self.height = int(screen_y / 9)
        self.x = x
        self.y = int(screen_y * 5 / 6)
        self.is_being_played = False
        if number % 12 == 1 or number % 12 == 4 or number % 12 == 6 or number % 12 == 9 or number % 12 == 11:
            #black note (A#/Bb , C#/Db , D#/Eb , F#/Gb , G#/Ab)
            self.color = (0, 0, 0)
        else:
            #white note (A , B , C , D , E , F , G)
            self.is_white_note = True
            self.color = (255, 255, 255)
            self.lower_width = self.width
            self.lower_x = x
            if number % 12 == 0 or number % 12 == 2 or number % 12 == 5 or number % 12 == 7 or number % 12 == 10:
                #if there is a black note to the left,
                self.lower_x -= 10
                self.lower_width += 10
            if number % 12 == 0 or number % 12 == 3 or number % 12 == 5 or number % 12 == 8 or number % 12 == 10:
                #if there is a black note to the right,
                self.lower_width += 10

    def toggle(self, color):
        self.is_being_played = not self.is_being_played
        if self.is_being_played:
            self.color = color
        elif self.is_white_note:
            self.color = (255, 255, 255)
        else:
            self.color = (0, 0, 0)

    def draw(self, pygame, window):
        #upper part
        pygame.draw.rect(window, self.color, (self.x + 1, self.y, self.width - 2, self.height), 0)
        #lower part for white notes
        if self.is_white_note:
            pygame.draw.rect(window, self.color, (self.lower_x + 1, self.y + self.height, self.lower_width - 2, self.height), 0)