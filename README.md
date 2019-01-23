# MIDI_Visualizer
## ![Example Usage](examples/videos/SNK_vid.gif)
## Inputs
```
python ./MIDI_project.py --filepath ./test.mid --title My Song --subtitle The Best --composer Bachobel --arranger Copyright Infringing Guy --tbs 1.2 --tbe 1.4 --spd 5 --rcd Y
```
In command line, MIDI_Visualizer uses a parser to parse commands from the user.

```--filepath``` takes the path to the midifile to visualize.  
```--tbs``` takes a float of time (seconds) before the visualizer receives the first message.  
```--tbe``` takes a float of time (seconds) before the visualizer ends the program after receiving the final message.  
```--spd``` takes an int and affects the downward speed of the notes.  
```--rcd``` takes a Y/N input and affects whether the program records and outputs the visualization as an mp4 file to the video folder.  
```--title```, ```--subtitle```, ```--composer``` and ```--arranger``` take in strings that appear in an intro sequence.
```--col1``` takes a hex color code i.e. "#00CC00" 


##Known Problems
On MacOS, the code 
```
player = pygame.midi.Output(0)
player.set_instrument(0)
```
does not work. Follow the instructions @ https://stackoverflow.com/questions/49543366/why-pygame-midi-doesnt-work-on-macos-whereas-pygame-mixer-does

