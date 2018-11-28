import mido

pathToMidi = "./Fukashigi_no_Carte_Shinkai_Ver..mid"

mid = mido.MidiFile(pathToMidi)
for msg in mid.play():
    print(msg)
