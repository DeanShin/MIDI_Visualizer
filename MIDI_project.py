import mido

pathToMidi = "./Fukashigi_no_Carte_Shinkai_Ver..mid"
from note import Note

notes = []

mid = mido.MidiFile(pathToMidi)
    
for msg in mid.play(meta_messages=True):
    if ! msg.isMeta:
        notes.append(Note(msg.channel, msg.type, msg.velocity, msg.time))
    
    
