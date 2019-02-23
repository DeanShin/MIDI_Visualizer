# MIDI_Visualizer
## ![Example Usage](examples/videos/SNK_vid.gif)
## Inputs

```python ./MIDI_project.py --tbs 1.2 --tbe 1.4 --spd 5 --rcd Y```

In command line, MIDI_Visualizer uses a parser to parse commands from the user.

```--tbs``` takes a float of time (seconds) before the visualizer receives the first message.  
```--tbe``` takes a float of time (seconds) before the visualizer ends the program after receiving the final message.  
```--spd``` takes an int and affects the downward speed of the notes.  
```--rcd``` takes a Y/N input and affects whether the program records and outputs the visualization as an mp4 file to the video folder.  
```--col1``` takes a hex color code i.e. "#00CC00" 

## Known Problems

On MacOS, the code 
```
player = pygame.midi.Output(0)
player.set_instrument(0)
```
does not work. 

Open Spotlight Search and search Audio MIDI Setup;  
Open Audio MIDI Setup and press command+2  
This will open the 'MIDI Studio'.  
Double Click the IAC Driver icon.  
Click the checkbox that says 'Device is Online'.  
This will connect to any MIDI synthesizers you have downloaded--which if you haven't already, download a MIDI synthesizer online such as SimpleSynth or Reason.

## Code Description

MIDI_Visualizer uses a couple of external libraries--the most important one being Mido.  
Normally, when you try to open a MIDI file in, say, a text editor, it ends up looking like a jumbled *mess*:
![jumbled mess](/examples/screenshots/example-of-a-raw-midi-file.png)  
Not only that, but the MIDI docs are pretty unparseable themselves.  

This is why I decided to use an external library to parse my MIDI files.  
After researching my various options, **mido** seemed to be the simplest to implement into a program.
```import mido```  
From the Mido docs, "Mido is a library for working with MIDI messages and ports. It’s designed to be as straight forward and Pythonic as possible." 
