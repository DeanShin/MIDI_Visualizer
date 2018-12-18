import mido
import pygame
import pygame.midi
# Get key commands for input
from pygame.locals import *
from pygame import mixer
# sys module for terminating process
# Should replace end game with something like pygame.endgame or something
import sys
pathToMidi = "./From_our_Hearts_-_Timespinner_OST.mid"
pathToMP3 = ""
# from note_object import NoteObj
import time
import argparse
from datetime import datetime, date

parser = argparse.ArgumentParser()
parser.add_argument("--tbs", default="1", required=False, help="time before start")
args = parser.parse_args()
args = vars(args)

class NotePath():
    #this file holds the note_path class
    def __init__(self, number):
        self.x = number * 20
        self.y = 0
        self.notes = []
        self.deleteNote = False
        self.start_note = True
        self.piano_roll_obj = PianoRollObj(self.x, number)
        
    def toggle_note(self, channel, velocity):
        if self.start_note:
            self.notes.append(NoteObj(self.x, channel, velocity))
        else:
            self.notes[-1].stop_growing()
        self.start_note = not self.start_note
        
    def update(self):
        if self.deleteNote:
            self.deleteNote = False
            del(self.notes[0])
        for n, i in enumerate(self.notes):
            i.move()
            i.draw()
            #triggers deletion flag once note travels off screen
            if i.y >= surface_dims[1]:
                self.deleteNote = True
        #delete note           

        self.piano_roll_obj.draw()

class NoteObj():
    # this file holds the note class 
    def __init__(self, x, channel, velocity):
        self.height = 0
        self.width = 20
        self.x = x
        self.y = 0
        self.change_y = 5
        #making note brighter as velocity increases
        self.color = (255, velocity * 2, 255 - velocity * 2)
        self.thickness = 2
        self.is_still_growing = True
        
    def stop_growing(self):
        self.is_still_growing = False
        
    def move(self):
        if self.is_still_growing:
            self.height += self.change_y
        else: 
            self.y += self.change_y
        
    def draw(self):
        #print("drawing " + str(self.x) + " " + str(self.y))
        #innards
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)
        #shell
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height), self.thickness)
        
class PianoRollObj():
    def __init__(self, x, number):

        self.is_white_note = False
        self.width = 20
        self.height = int(surface_dims[1] / 16)
        self.x = x
        self.y = int(surface_dims[1] * 7 / 8)



        if number % 12 == 1 or number % 12 == 4 or number % 12 == 6 or number % 12 == 9 or number % 12 == 11:
            #black note (A#/Bb , C#/Db , D#/Eb , F#/Gb , G#/Ab)
            self.color = (0, 0, 0)
        else:
            #white note (A , B , C , D , E , F , G)
            self.is_white_note = True
            self.color = (255, 255, 255)
            self.lower_width = self.width
            self.lower_x = x
            if number % 12 == 0 or number % 12 == 2 or number % 12 == 5 or number % 12 == 7 or number % 12 == 10:
                self.lower_x -= 10
                self.lower_width += 10
            if number % 12 == 0 or number % 12 == 3 or number % 12 == 5 or number % 12 == 8 or number % 12 == 10:
                self.lower_width += 10

    def draw(self):
        #upper part
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)
        #lower part for white notes
        if self.is_white_note:
            pygame.draw.rect(surface, self.color, (self.lower_x, self.y + self.height, self.lower_width, self.height), 0)

pygame.init()
pygame.display.set_caption('MIDI Project')
surface_dims = (1760, 990)
surface = pygame.display.set_mode(surface_dims)
background = (63,63,63)
FPS = 60
clock = pygame.time.Clock()

mid = mido.MidiFile(pathToMidi)
note_paths = []
i = 0
j = 0

pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)

time.sleep(float(args["tbs"]))

start_time = time.time()
next_spawn_time = start_time

#mido.merge_tracks(mid.tracks)

iterable = iter(mid)
msg = next(iterable) 

while j < 88:
    note_paths.append(NotePath(j))
    j += 1
    # print("spawn" + str(j))

try: 
    mixer.init()
    mixer.music.load(pathToMP3)
    mixer.music.play()
except:
    pass

stop_reading = False

while True:
    try:
        while time.time() >= next_spawn_time and not stop_reading:
            print(msg)
            if msg.type == 'note_on':
                note_paths[msg.note - 21].toggle_note(msg.channel, msg.velocity)
                player.note_off(msg.note, msg.velocity, msg.channel)
                player.note_on(msg.note, msg.velocity, msg.channel)
            elif msg.is_meta == False:
                if msg.type == 'control_change':
                    #sustain pedal
                    if msg.control == 64:
                        #if msg.value is 0-63, then pedal turns off. Otherwise, (64-127) turn on. 
                        if msg.value < 64: 
                            print("PEDAL OFF")
                        else:
                            print("PEDAL ON")
                    else:
                        print("Unimplemented control change" + "\n" + "\n")
                elif msg.type == 'program_change':
                    pass
                else:
                    print("Unimplemented message type" + "\n" + "\n")

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
                    stop_reading = True
                
                else:
                    print("Unimplemented MetaMessage" + "\n \n")
                
            msg = next(iterable)
            next_spawn_time = next_spawn_time + msg.time 
            
            #info printing
            
            today = datetime.fromtimestamp(next_spawn_time)
            now = " ".join((str(today.date()),str(today.time())))
            print(now)
            
    except StopIteration:
        break
    # # Save every frame
    # filename = "Snaps/%04d.png" % file_num
    # pygame.image.save(surface, filename)

    # Process Events
    for e in pygame.event.get():
        if e.type == KEYUP: # On User Key Press Up
            if e.key == K_ESCAPE:# End Game
                sys.exit()

    # file_num = file_num + 1
    pygame.display.flip()
    clock.tick(FPS)

    #draw and move
    
    surface.fill(background)
    for note_path in note_paths:
        note_path.update()
        
