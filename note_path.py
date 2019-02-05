from note_obj import NoteObj
from piano_roll_obj import PianoRollObj

#this file holds the NotePath class

class NotePath():

    def __init__(self, note_id, screen, spd, col1, col2):
        self.is_sustain = False
        self.piano_y_pos = int(screen[1] * 5 / 6)
        if note_id is -1:
            self.width = screen[0]
            self.x = 0
            self.is_sustain = True
        else:
            self.width = screen[0] / 88
            self.x = note_id * self.width
            self.piano_roll_obj = PianoRollObj(self.x, note_id, screen)
        self.notes = []
        self.deleteNote = False
        self.start_note = True
        self.note_id = note_id
        self.y = 0
        self.spd = spd
        self.col1 = col1
        self.col2 = col2


    def toggle_note(self, channel, velocity, lin_map_vel, offset):
        if self.start_note:
            self.notes.append(NoteObj(self.note_id, channel, velocity, lin_map_vel, \
            self.spd, self.is_sustain, self.width, self.col1, self.col2, offset))
        else:
            self.notes[-1].stop_growing(offset)
        self.start_note = not self.start_note

    def draw_piano(self, pygame, window):
        if not self.is_sustain:
            self.piano_roll_obj.draw(pygame, window)

    def update(self, pygame, window, player):
        if self.deleteNote:
            self.deleteNote = False
            del(self.notes[0])
        for n, i in enumerate(self.notes):
            i.move()
            i.draw(pygame, window)
            # plays note when note collides with piano roll
            if i.y + i.height >= self.piano_y_pos and not i.shrinking:
                i.start_shrinking()
                if not self.is_sustain:
                    self.piano_roll_obj.toggle(i.color)
                    player.note_on(i.note_id + 21, i.velocity, i.channel)
            # stops playing and deletes note when note passes piano roll
            if i.y >= self.piano_y_pos:
                self.deleteNote = True
                if not self.is_sustain:
                    self.piano_roll_obj.toggle(i.color)
                    player.note_off(i.note_id + 21, i.velocity, i.channel)