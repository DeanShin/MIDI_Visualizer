import mido

pathToMidi = "./Fukashigi_no_Carte_Shinkai_Ver..mid"
from note import Note

screen_dims = (1760, 990)
surface = pygame.display.set_mode(screen_dims)
notes = []
mid = mido.MidiFile(pathToMidi)

# parse MIDI file and spawn notes in actual time
for msg in mid.play(meta_messages=True):
    if ! msg.isMeta:
        notes.append(Note(msg.channel, msg.type, msg.velocity, msg.time))
    else
        print(msg)
# draw     
while true:
    for noteObject in notes:
        noteObject.draw()
        
