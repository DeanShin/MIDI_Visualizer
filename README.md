# MIDI_Visualizer
## ![Example Usage](/SNK_vid.gif)
## Inputs
```
python ./MIDI_project.py --midiname ./test.mid --tbs 1.2 --tbe 1.4 --spd 5 --rcd Y
```
In command line, MIDI_Visualizer uses a parser to recieve inputs from the user.

input ```--midiname``` takes the path to the midifile to visualize.
input ```--tbs``` takes a float of time (seconds) before the visualizer receives the first message
input ```--tbe``` takes a float of time (seconds) before the visualizer ends the program after receiving the final message
input ```--spd``` takes an int and affects the downward speed of the notes
input ```--rcd``` takes a Y/N input and affects whether the program records the visualization
