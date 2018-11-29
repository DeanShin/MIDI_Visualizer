import mido
import pygame

pathToMidi = "./Fukashigi_no_Carte_Shinkai_Ver..mid"
from note_track import NoteTrack
from note_object import NoteObj

screen_dims = (1760, 990)
surface = pygame.display.set_mode(screen_dims)

mid = mido.MidiFile(pathToMidi)
note_tracks = []
j = 0

while j < 88
    note_tracks.append(NoteTrack(j))
    j += 1
    print("spawn" + str(j))

# parse MIDI file and spawn notes in actual time
for msg in mid.play(meta_messages=True):
    
    print(msg)

    if msg.type == 'note_on':
        print
        note_tracks[msg.note - 21].start_note(msg.channel, msg.velocity)
    
    elif msg.type == 'note_off':
        note_tracks[msg.note - 21].stop_note()
        
    elif msg.is_meta == False:
        pass
    else:
        #is metaMessage
        
        #attrs = vars(msg)
        #print(attrs)
        if msg.type == 'text':
            pass
        elif msg.type == 'copyright':
            pass
        elif msg.type == 'set_tempo':
            pass
        elif msg.type == 'time_signature':
            pass
        elif msg.type == 'end_of_track':
            pass
        else:
            pass
# draw & update notes
while true:
    for i in note_tracks:
        i.update()
        
