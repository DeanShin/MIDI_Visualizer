# MIDI_Visualizer
## ![Example Usage](examples/videos/sample_midi.gif)
## Inputs
### Usage

```python ./MIDI_project.py --tbs 1.2 --tbe 1.4 --spd 5 --rcd Y```

In command line, MIDI_Visualizer uses a parser to parse commands from the user.

```--tbs``` takes a float of time (seconds) before the visualizer receives the first message.  
```--tbe``` takes a float of time (seconds) before the visualizer ends the program after receiving the final message.  
```--spd``` takes an int and affects the downward speed of the notes.  
```--rcd``` takes a Y/N input and affects whether the program records and outputs the visualization as an mp4 file to the video folder.  
```--col1``` takes a hex color code i.e. "#00CC00" 

## Known Problems

On MacOS, the code 
```python
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

### Fundamentals

MIDI_Visualizer uses a couple of external libraries--the most important one being Mido.  
Normally, when you try to open a [**MIDI**](https://www.midi.org/) file in, say, a text editor, it ends up looking like a jumbled *mess*:  

![jumbled mess](/examples/screenshots/example-of-a-raw-midi-file.png)  

Not only that, but the MIDI docs are pretty unparseable themselves.  

This is why I decided to use an external library to parse my MIDI files. After researching my various options, [**Mido**](https://mido.readthedocs.io/en/latest/) seemed to be the simplest to implement into a program.  

```import mido```  

From the Mido docs, "Mido is a library for working with MIDI messages and ports. It’s designed to be as straight forward and Pythonic as possible." The Mido site has a couple of example programs, one of which served as the basis for my code:  

```python
mid = mido.MidiFile('song.mid')
for msg in mid.play():
    port.send(msg)
```

Which I changed into  

```python
mid = mido.MidiFile(filepath)
for msg in mid.play():
    print(msg)
```

The first line, ```mid = mido.MidiFile(pathToMidi)```, makes ```MidiFile``` object ```mid``` from a MIDI file located at a certain ```filepath```. ```mid``` contains ```messages```, which can then be iterated through, i.e. ```for msg in mid.play()```.  

```mid.play()``` is a function that outputs messages, waiting for the correct amount of time according to each message's ```time``` attribute. This function is good and all for normal and simple usage, however as you'll see later, there are many problems that appear later.

![phase1](/examples/screenshots/phase1.png)  

There are several types of messages, the largest sub-divisions being ```messages``` and ```meta_messages```, ```meta_messages``` hold special information such as when the pedal turns on/off, or lyrics, or the name of an instrument; therefore the ```mid.play()``` function by default does not output ```meta_messages```.  

While there are many types of messages and meta_messages, the two most common are `note_on` and `note_off`. Every `note_on` and `note_off` message has 5 variables: `type`, `channel`, `note`, `velocity`, and `time`.

Example messages:  
```
note_on channel=0 note=90 velocity=80 time=0.03125
control_change channel=0 control=64 value=127 time=0.05
```  
a note_on type message:  
```python
type=note_on    # the type of the message
channel=0       # analagous with TV or radio channels
note=90         # the pitch of a note, where note=60 equals middle C
velocity=80     # affects the loudness and timbre of a note, basically, how hard a note is played
time=0.03125    # how many seconds have passed since the last message
```  
a control_change type message:  
```python
type=control_change
channel=0
control=64      # what function to perform: i.e. control=64 signifies that the sustain pedal should be sent a value
value=127       # what value to send
time=0.05
```

Strangely, many MIDI files do not utilize the ```note_off``` type message. Instead, two ```note_on``` type messages are sent--the first one signifies the start of the note, the second one signifies the end. In this system, you can not activate a note that is already activated.  

With a couple (read: _lots_) of `if` statements, you can easily separate all message types into performing unique functions:
```python
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

---

The next step after parsing the MIDI files is to find some way to display them. Following the tried and true methods, I took programs such as [**Synthesia**](https://www.synthesiagame.com/) as inspiration for my own program.  

But first of all, how do you display something in python? The answer is a library such as [**pygame**](https://www.pygame.org/news).  

Pygame is a bit complicated to get in to, however once you learn the basics, it is extremely easy to quickly implement visuals into a program. There are a couple of fundamental lines of code that are necessary for many programs in ```pygame```.  

To initialize,
```python
pygame.init()                                   # initialize all imported pygame modules
pygame.display.set_caption('MIDI Project')      # set the current window caption
window_dims = (1760, 990)                       # width and height
window = pygame.display.set_mode(window_dims)   # initialize a window or screen for display
background = (63,63,63)                         # a color, in this case, in RGB.
FPS = 30.0                                      # frames per second
clock = pygame.time.Clock()                     # create an object to help track time
```
then, in a loop,
```python
while True:
    pygame.display.flip()                       # update the full display Surface to the screen
    clock.tick(FPS)                             # update the clock
    window.fill(background)                     # fill Surface with a solid color
```
This will create a basic gray background that updates at a max of 30.0 frames per second. You can then ```pygame.Surface.blit()``` one surface onto another surface (think of it like pasting one image on top of another), or ```pygame.draw.rect()``` to draw a rectangle onto a given surface.

The majority of my visualizer is comprised of rectangles, so ```pygame.draw.rect()``` gets a _lot_ of use.  

---

The final necessary thing to do is to have some way to _play_ the notes--luckily, pygame is host to a library that allows us to do just that aptly named [**pygame.midi**](https://www.pygame.org/docs/ref/midi.html). Implementing this library is easy as well:

```python
pygame.midi.init()
try:
    player = pygame.midi.Output(0)
except:
    player = pygame.midi.Output(1)
player.set_instrument(0)
```

---

## Structure  

With all of this information, as there are notable 'objects' (i.e. piano keys, piano notes) to be programmed, I decided to make my program object-oriented. 

As mentioned above, there are two obvious classes that I should implement: `PianoRollObj`, the piano roll, and the falling notes being the other. However, we can simplify things further--as notes (at least in my program) do not change in pitch, there are distinct vertical 'paths' that these notes follow--beginning from the top of the screen, and ending at the piano keyboard, notes follow _note paths_, (vertical lines with a constant x value) until they collide with the piano keyboard and get played.

A NotePath consists of one piano key and an array of the notes that fall onto it `notes[]`. As there are 88 keys on your standard piano, (plus one for the sustain pedal) there are 89 NotePath objects in the array ```note_paths[]```.
```python
i = 0
note_paths = []
while i < 89:
    #i - 1 in NotePath() accounts for NotePath 0 being the path for the pedal
    note_paths.append(NotePath(i - 1, window_dims, int(args["spd"]), col1, col2, BUBBLES))
    i += 1
del(i, col1, col2)
```  

Each ```NotePath``` object holds an array ```notes``` that comprises of active (currently being drawn) ```NoteObj```:  
```self.notes = [NoteObj]```  

...and a ```PianoRollObj``` corresponding to the position of the NotePath in the array:  
```self.piano_roll_obj = PianoRollObj(self.x, note_id, window)```  

A ```NotePath``` is responsible for spawning, updating, and deleting every `NoteObj` that shares its `note` value. The ```NotePath``` therefore holds much of the information required for doing so:  
```python
def __init__(self, note_id, window, spd, col1, col2):
    self.width = window[0] / 88
    self.x = note_id * self.width
    self.y = 0
    self.spd = spd
    self.note_id = note_id
    self.col1 = col1
    self.col2 = col2
```  
Thus when a note needs to be spawned, only the bare amount of inputs are needed.  

Whenever a note_on or note_off type message is read, the `NotePath` corresponding with the `note` value of the MIDI message has the function `toggle_note()` called.  
```python
if msg.type == 'note_on' or msg.type == 'note_off':
    # A0 (note_path[1]) is msg.note == 21
    # Therefore in order to reference the correct note_path, the equation becomes msg.note + 1 - 21.
    note_paths[msg.note + 1 - 21].toggle_note(msg.channel, msg.velocity, \
    lin_map_vel(msg.velocity), int((current_time - next_msg_time) / frame_length * spd))
```  
```
def toggle_note(self, channel, velocity, lin_map_vel, offset):
    if self.start_note:
        self.notes.append(NoteObj(self.note_id, channel, velocity, lin_map_vel, \
        self.spd, self.is_sustain, self.width, self.col1, self.col2, offset))
    else:
        self.notes[-1].stop_growing(offset)
    self.start_note = not self.start_note
```  
Each ```NoteObj``` falls at a certain speed, and has a certain color calculated according to the ```velocity``` of the note that has been linearly mapped.  
```python
def lin_map_vel(velocity):
    if velocity == 0:
        return 0
    else:
        return (float(velocity - min_vel)/float(max_vel - min_vel + 1))
```   
```python
def __init__(lin_map_vel, col1, col2):
    # making note color change as velocity changes, 
    # minimum velocity == col1, maximum velocity == col2
    self.color = (int(col1[0] + lin_map_vel * (col2[0] - col1[0])), \
    int(col1[1] + lin_map_vel * (col2[1] - col1[1])), \
    int(col1[2] + lin_map_vel * (col2[2] - col1[2])))
```  
As we are reading through the messages in real time, we do not know how long the note is going to be held when we initialize the `NoteObj`. Consequently, we cannot pre-determine the height of the `NoteObj` and have the Object start off-screen.  

What we can do, however, is (while the note is being played) have the `NoteObj`'s height increase:

```python
def update(self):
    if self.growing:
        self.height += self.change_y
```  

This creates the illusion that the `NoteObj` is falling, when, in fact, it is simply increasing in height.  

When the note is released (when the second note_on message is received), we stop the note from increasing in height and instead change the object's y value:  

```python
def update(self):
    if self.growing:
        self.height += self.change_y
    else:
        self.y += self.change_y
```

That covers the first half of the note, however what about the latter half?  

```python
def update(self, pygame, window, player):
    if self.deleteNote:
        self.deleteNote = False
        del(self.notes[0])
    for n, i in enumerate(self.notes):
        # plays note when note collides with piano roll
        if i.y + i.height >= self.piano_y_pos and not i.shrinking:
            i.start_shrinking()
            if not self.is_sustain:
                self.piano_roll_obj.toggle(i.color)
                player.note_on(i.note_id + 21, i.velocity, i.channel)
        # stops playing and deletes note when note passes piano roll
        if i.y >= self.piano_y_pos:
            self.deleteNote = True
            if not self.is_sustain:
                self.piano_roll_obj.toggle(i.color)
                player.note_off(i.note_id + 21, i.velocity, i.channel)
```  

Here, there are two main phases as well:  

When the bottom of the note comes into contact with the piano keyboard, we want to do two things: play, and shrink. 
When the `shrinking` boolean is True, the note, in addition to moving downwards every frame, reduces in height.  

```python
def update(self):
    if self.growing:
        self.height += self.change_y
    else:
        self.y += self.change_y
        if self.shrinking:
            self.height -= self.change_y
```
