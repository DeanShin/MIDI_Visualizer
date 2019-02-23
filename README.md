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

This is why I decided to use an external library to parse my MIDI files. After researching my various options, **Mido** seemed to be the simplest to implement into a program.  

```import mido```  

From the Mido docs, "Mido is a library for working with MIDI messages and ports. It’s designed to be as straight forward and Pythonic as possible." The Mido site has a couple of example programs, one of which served as the basis for my code:  

```
mid = mido.MidiFile('song.mid')
for msg in mid.play():
    port.send(msg)
```

Which I changed into  

```
mid = mido.MidiFile(filepath)
for msg in mid.play():
    print(msg)
```

The first line, ```mid = mido.MidiFile(pathToMidi)```, makes ```MidiFile``` object ```mid``` from a MIDI file located at a certain ```filepath```. ```mid``` contains ```messages```, which can then be iterated through, i.e. ```for msg in mid.play()```.  

```mid.play()``` is a function that outputs messages, waiting for the correct amount of time according to each message's ```time``` attribute. This function is good and all for normal and simple usage, however as you'll see later, there are many problems that appear later.

![phase1](/examples/screenshots/phase1.png)  

(Note: there are several types of messages, the largest sub-divisions being ```messages``` and ```meta_messages```, ```meta_messages``` hold special information such as when the pedal turns on/off, or lyrics, or the name of an instrument; therefore the ```mid.play()``` function by default does not output ```meta_messages```.)  

With a couple (read: _lots_) of `if` statements, you can easily separate all message types into performing unique functions:
```
if msg.type == 'note_on' or msg.type == 'note_off':
    #DO SOMETHING
    pass
elif msg.is_meta == False:
    if msg.type == 'control_change':
        #SUSTAIN PEDAL
        if msg.control == 64:
            pass
        else:
            print("Unimplemented control change" + "\n" + "\n")
    else:
        print("Unimplemented message type" + "\n" + "\n")
else:
    #is metaMessage
    print("Unimplemented MetaMessage" + "\n \n")
```  

The next step after parsing the MIDI files is to find some way to display them. Following the tried and true methods, I took programs such as Synthesia as inspiration for my own program.  
But first, how do you display something in python? The answer is a library such as ```pygame```.  
Pygame is a bit complicated to get in to, however once you learn the basics, it is extremely easy to quickly implement visuals into a program.  
There are a couple of fundamental lines of code that are necessary for many programs in ```pygame```.  
To initialize,  
```
pygame.init()
pygame.display.set_caption('MIDI Project')
window_dims = (1760, 990) # width and height
window = pygame.display.set_mode(window_dims)
background = (63,63,63) # a color, in this case, in RGB.
FPS = 30.0
clock = pygame.time.Clock()
```  
then, in a loop,
```
while True:
    pygame.display.flip()
    clock.tick(FPS)
    window.fill(background)
```
