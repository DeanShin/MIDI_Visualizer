from note_obj import NoteObj
from piano_roll_obj import PianoRollObj
from bubble import Bubble

#this file holds the NotePath class

class NotePath():

    def __init__(self, note_id, window, spd, col1, col2, BUBBLES):
        self.is_sustain = False
        self.piano_y_pos = int(window[1] * 5 / 6)
        if note_id is -1:
            self.width = window[0]
            self.x = 0
            self.is_sustain = True
        else:
            self.width = window[0] / 88
            self.x = note_id * self.width
            self.piano_roll_obj = PianoRollObj(self.x, note_id, window)
        self.notes = []
        self.bubbles = []
        self.deleteNote = False
        self.start_note = True
        self.note_id = note_id
        self.y = 0
        self.spd = spd
        self.col1 = col1
        self.col2 = col2
        self.do_bubbles = BUBBLES


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
    
    def draw_bubbles(self, pygame, window):
        for bubble in self.bubbles:
            bubble.draw(pygame, window)

    def update(self, pygame, window, player):
        if self.deleteNote:
            self.deleteNote = False
            del(self.notes[0])
        for n, i in enumerate(self.notes):
            i.update()
            i.draw(pygame, window)
            # plays note when note collides with piano roll
            if i.y + i.height >= self.piano_y_pos and not i.shrinking:
                i.start_shrinking()
                if not self.is_sustain:
                    self.piano_roll_obj.toggle(i.color)
                    player.note_on(i.note_id + 21, i.velocity, i.channel)
                    if self.do_bubbles:
                        self.bubbles.append(Bubble(pygame, window, self.notes[0].color, self.notes[0].velocity, \
                            self.x + self.width/2, self.piano_y_pos, self.width/2))
            # stops playing and deletes note when note passes piano roll
            if i.y >= self.piano_y_pos:
                self.deleteNote = True
                if not self.is_sustain:
                    self.piano_roll_obj.toggle(i.color)
                    player.note_off(i.note_id + 21, i.velocity, i.channel)
        if self.do_bubbles:
            for bubble in self.bubbles:
                if bubble.update():
                    del(self.bubbles[0])