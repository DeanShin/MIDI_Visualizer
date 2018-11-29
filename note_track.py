from note_object import NoteObj

class NoteTrack():
    #this file holds the note_track class
    def __init__(self, number):
        self.x = number * 20
        self.y = 0
        self.notes = []
        
    def start_note(self, channel, velocity):
        self.notes.append(NoteObj(this.x, channel, velocity))
        
    def stop_note(self):
        self.notes[-1].stop_growing
        
    def update(self):
        for i in self.notes:
            i.draw()
            i.move()
