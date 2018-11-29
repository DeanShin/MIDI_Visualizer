import mido
import pygame

pathToMidi = "./Fukashigi_no_Carte_Shinkai_Ver..mid"
from note_object import NoteObj

screen_dims = (1760, 990)
surface = pygame.display.set_mode(screen_dims)
notes = []
mid = mido.MidiFile(pathToMidi)

# parse MIDI file and spawn notes in actual time
for msg in mid.play(meta_messages=True):
    if msg.type == 'note_on':
        attrs = vars(msg)
        print(attrs)
        notes.append(NoteObj(msg.type, msg.time, msg.channel, msg.note, msg.velocity))
    elif msg.is_meta == False:
        pass
    else:
        print(msg)
# draw & update
while true:
    for i in notes:
        i.draw()
        i.move()
        
