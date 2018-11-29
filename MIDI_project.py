import mido
import pygame

pathToMidi = "./Fukashigi_no_Carte_Shinkai_Ver..mid"
from note_track import NoteTrack
from note_object import NoteObj

screen_dims = (1760, 990)
surface = pygame.display.set_mode(screen_dims)

mid = mido.MidiFile(pathToMidi)
note_tracks = [88]
i = 0

#initialize note_tracks
for note_track in note_tracks:
    note_tracks.append(NoteTrack(i))
    i++

# parse MIDI file and spawn notes in actual time
for msg in mid.play(meta_messages=True):
    
    if msg.type == 'note_on':
        note_tracks[msg.note - 21].start_note(msg.channel, msg.velocity)
    
    elif msg.type == 'note_off':
        note_tracks[msg.note - 21].stop_note()
        
    elif msg.is_meta == False:
        pass
    else:
        #is metaMessage
        print(msg)
        attrs = vars(msg)
        print(attrs)
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
# draw & update notes
while true:
    for i in note_tracks:
        i.update()
        
