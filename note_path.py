from note_obj import NoteObj
from piano_roll_obj import PianoRollObj

#this file holds the NotePath class

class NotePath():

    def __init__(self, note_id, screen_y, spd):
        self.note_id = note_id
        self.x = note_id * 20
        self.y = 0
        self.notes = []
        self.deleteNote = False
        self.start_note = True
        self.piano_roll_obj = PianoRollObj(self.x, note_id, screen_y)
        self.piano_y_pos = self.piano_roll_obj.y
        self.spd = spd

    def toggle_note(self, channel, velocity, lin_map_vel):
        if self.start_note:
            self.notes.append(NoteObj(self.note_id, channel, velocity, lin_map_vel, self.spd))
        else:
            self.notes[-1].stop_growing()
        self.start_note = not self.start_note

    def draw_piano(self, pygame, surface):
        self.piano_roll_obj.draw(pygame, surface)

    def update(self, pygame, surface, player):
        if self.deleteNote:
            self.deleteNote = False
            del(self.notes[0])
        for n, i in enumerate(self.notes):
            i.move()
            i.draw(pygame, surface)
            # plays note when note collides with piano roll
            if i.y + i.height >= self.piano_y_pos and not i.shrinking:
                i.start_shrinking()
                self.piano_roll_obj.toggle(i.color)
                player.note_on(i.note_id + 21, i.velocity, i.channel)
            # stops playing and deletes note when note passes piano roll
            if i.y >= self.piano_y_pos:
                self.deleteNote = True
                self.piano_roll_obj.toggle(i.color)
                player.note_off(i.note_id + 21, i.velocity, i.channel)