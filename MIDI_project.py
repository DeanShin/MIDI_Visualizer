import mido
import pygame
import pygame.midi
# sys module for terminating process
# Should replace end game with something like pygame.endgame or something
import sys
import time
# Get key commands for input
import argparse
import os

from pygame.locals import *
from pygame import mixer
from datetime import datetime, date

from note_path import NotePath
from note_obj import NoteObj

pathToMidi = "./SNK.mid"
pathToMP3 = ""

parser = argparse.ArgumentParser()
parser.add_argument("--midiname", default=str(pathToMidi), required=False, help="path to midi file")
parser.add_argument("--tbs", default="1", required=False, help="time before start")
parser.add_argument("--tbe", default="3", required=False, help="time before end")
parser.add_argument("--spd", default="5", required=False, help="speed of notes")
parser.add_argument("--title", default="N/A", required=False, help="title of piece")
args = parser.parse_args()
args = vars(args)

pathToMidi = args["midiname"]

pygame.init()
pygame.display.set_caption('MIDI Project')
surface_dims = (1760, 990)
surface = pygame.display.set_mode(surface_dims)
background = (63,63,63)
FPS = 60
clock = pygame.time.Clock()

pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)

mid = mido.MidiFile(pathToMidi)
note_paths = []

min_vel = 127
max_vel = 0

file_num = 0

try:
    os.makedirs("Snaps")
except OSError:
    pass


#mido.merge_tracks(mid.tracks)

def lin_map_vel(velocity):
    return (float(velocity - min_vel)/float(max_vel - min_vel + 1)) * 255

def draw_all():
    surface.fill(background)
    for note_path in note_paths:
        note_path.update(pygame, surface, player)
    pygame.draw.rect(surface, background, (0, int(surface_dims[1]*5/6), surface_dims[0], int(surface_dims[1]/6)), 0)
    for note_path in note_paths:
        note_path.draw_piano(pygame, surface)


# find minimum and maximum values of velocity
list_of_vel = []
for msg in mid:
    if msg.type is 'note_on' and msg.velocity is not 0 and msg.type is not 'note_off':
        list_of_vel.append(msg.velocity)
for vel in list_of_vel:
    if min_vel > vel:
        min_vel = vel
    if max_vel < vel:
        max_vel = vel
del(list_of_vel)

i = 0
while i < 88:
    note_paths.append(NotePath(i, surface_dims[1], int(args["spd"])))
    i += 1
del(i)

# INTRO

next_msg_time = time.time() + float(args["tbs"])
while time.time() < next_msg_time:
    pygame.display.flip()
    clock.tick(FPS)
    draw_all()

mid = mido.MidiFile(pathToMidi)
iterable = iter(mid)
msg = next(iterable) 

# PLAY

try: 
    mixer.init()
    mixer.music.load(pathToMP3)
    mixer.music.play()
except:
    pass

next_msg_time = time.time()
stop_reading = False
started_ending = False

while True:
    try:
        while time.time() >= next_msg_time and not stop_reading:
            print(msg)
            if msg.type == 'note_on' or msg.type == 'note_off':
                note_paths[msg.note - 21].toggle_note(msg.channel, msg.velocity, lin_map_vel(msg.velocity))
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
            
            #iterate to the next message

            msg = next(iterable)
            next_msg_time = next_msg_time + msg.time 
            
            #info printing
            
            today = datetime.fromtimestamp(next_msg_time)
            now = " ".join((str(today.date()),str(today.time())))
            print(now)
            
    except StopIteration:
        #when there are no more messages, trigger a countdown of length tbe\
            next_msg_time = next_msg_time + int(args["tbe"])
            started_ending = True

    finally:
        # Save every frame
        filename = "Snaps/%04d.png" % file_num
        pygame.image.save(surface, filename)
        file_num = file_num + 1

        # Process Events
        for e in pygame.event.get():
            if e.type == KEYUP: # On User Key Press Up
                if e.key == K_ESCAPE:# End Game
                    sys.exit()

        
        pygame.display.flip()
        clock.tick(FPS)

        #draw and move
        
        draw_all()

        if started_ending:
            if time.time() >= next_msg_time:
                print("END")
                break

# OUTRO

from subprocess import call
meth = "python3 tk-img2video.py -d ./images -o ./videos/new_video.mp4 -e jpg -t 60"
call([meth.split()])