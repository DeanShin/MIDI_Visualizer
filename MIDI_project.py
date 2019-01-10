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

pathToMidi = "./examples/midifiles/SNK.mid"
pathToMP3 = ""

parser = argparse.ArgumentParser()
parser.add_argument("--filepath", default=str(pathToMidi), required=False, help="str  path to midi file")
parser.add_argument("--title", default="Intuition and Insight", required=False, help="str  title of piece")
parser.add_argument("--subtitle", default="Sen no Kiseki IV", required=False, help="str  subtitle")
parser.add_argument("--composer", default="Mitsuo Singa", required=False, help="str  composer")
parser.add_argument("--arranger", default="Me", required=False, help="str  arranger")
parser.add_argument("--tbs", default="1", required=False, help="float  time before start")
parser.add_argument("--tbe", default="3", required=False, help="float  time before end")
parser.add_argument("--spd", default="5", required=False, help="int  speed of notes")
parser.add_argument("--rcd", default="N", required=False, help="bool  recording, inputs Y/N")
args = parser.parse_args()
args = vars(args)

if args["rcd"] is "Y":
    is_recording = True
else:
    is_recording = False
pathToMidi = args["filepath"]

pygame.init()
pygame.display.set_caption('MIDI Project')
surface_dims = (1760, 990)
surface = pygame.display.set_mode(surface_dims)
background = (63,63,63)
FPS = 60.0
frame_length = 1/FPS
clock = pygame.time.Clock()

pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)

mid = mido.MidiFile(pathToMidi)
note_paths = []

min_vel = 127
max_vel = 0

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

if is_recording:
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

i = 0
while i < 89:
    #i - 1 in NotePath() accounts for NotePath 0 being the path for the pedal
    note_paths.append(NotePath(i - 1, surface_dims[1], int(args["spd"])))
    i += 1
del(i)

# INTRO
font_T = pygame.font.Font("resources/fonts/SoukouMincho.ttf", 100)
text_T = font_T.render(args["title"], True, (255, 255, 255))
font_t = pygame.font.Font("resources/fonts/SoukouMincho.ttf", 70)
text_t = font_t.render(args["subtitle"], True, (255, 255, 255))
font_lilt = pygame.font.Font("resources/fonts/SoukouMincho.ttf", 40)
text_lilt = font_lilt.render("Composed by " + args["composer"] + ", Arranged by " + args["arranger"] + ".", True, (255,255,255))

current_time = 0
next_msg_time = float(args["tbs"])
while current_time < next_msg_time:
    pygame.display.flip()
    clock.tick(FPS)
    draw_all()
    surface.blit(text_T, (surface_dims[0]/2 - text_T.get_width() // 2, surface_dims[1]/2 - text_T.get_height() // 2 - 70))
    surface.blit(text_t, (surface_dims[0]/2 - text_t.get_width() // 2, surface_dims[1]/2 - text_t.get_height() // 2))
    surface.blit(text_lilt, (surface_dims[0]/2 - text_lilt.get_width() // 2, surface_dims[1]/2 - text_lilt.get_height() // 2 + 55))
    current_time = current_time + frame_length
    #print(current_time)

del text_T
del text_t

mid = mido.MidiFile(pathToMidi)
iterable = iter(mid)
msg = next(iterable)

# PLAY


    # try:
    #     mixer.init()
    #     mixer.music.load(pathToMP3)
    #     mixer.music.play()
    # except:
    #     pass

next_msg_time = 0
current_time = 0
stop_reading = False
started_ending = False

while True:
    try:
        while current_time >= next_msg_time and not stop_reading:
            print(msg)
            if msg.type == 'note_on' or msg.type == 'note_off':
                #A0 (note_path[1]) is msg.note == 21
                note_paths[msg.note + 1 - 21].toggle_note(msg.channel, msg.velocity, lin_map_vel(msg.velocity))
            elif msg.is_meta == False:
                if msg.type == 'control_change':
                    #sustain pedal
                    if msg.control == 64:
                        #if msg.value is 0-63, then pedal (note_path[0]) turns off. 
                        #Otherwise, (64-127) turn on.
                        note_paths[0].toggle_note(0, 0, 0)
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

            #today = datetime.fromtimestamp(next_msg_time)
            #now = " ".join((str(today.date()),str(today.time())))
            #print(now)

    except StopIteration:
        #when there are no more messages, trigger a countdown of length tbe\
            next_msg_time = next_msg_time + int(args["tbe"])
            started_ending = True

    finally:
        # Save every frame
        if is_recording:
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
        current_time = current_time + frame_length

        #draw and move

        draw_all()

        if started_ending:
            if time.time() >= next_msg_time:
                print("END")
                break

# OUTRO

if is_recording:
    from subprocess import call
    meth = "python3 tk-img2video.py -d ./images -o ./videos/new_video.mp4 -e jpg -t 60"
    call([meth.split()])
