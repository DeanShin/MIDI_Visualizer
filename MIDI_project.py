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
from button import Button
from input_box import InputBox

parser = argparse.ArgumentParser()
parser.add_argument("--rfd", default="N", required=False, help="bool  record notes live from a connected device")
parser.add_argument("--tbs", default="1", required=False, help="float  time before start")
parser.add_argument("--tbe", default="3", required=False, help="float  time before end")
parser.add_argument("--spd", default="5", required=False, help="int  speed of notes")
parser.add_argument("--rcd", default="N", required=False, help="bool  recording, inputs Y/N")
parser.add_argument("--col1", default="#FFFFFF", required=False, help="color (hex) of lowest velocity notes")
parser.add_argument("--col2", default="#000000", required=False, help="color (hex) of highest velocity notes")
args = parser.parse_args()
args = vars(args)

if args["rfd"] is "Y":
    live_input = True
else:
    live_input = False
if args["rcd"] is "Y":
    is_recording = True
else:
    is_recording = False

pygame.init()
pygame.display.set_caption('MIDI Project')

try:
    from screeninfo import get_monitors
    for i, m in enumerate(get_monitors()):
        if i == 0:
            monitor_width = m.width
            monitor_height = m.height
    window_dims = (1760, 990)
    if monitor_width < 1760 or monitor_height < 990:
        window_dims = (880, 445)
except:
    print("Screensize detection failed.")
    window_dims = (1760, 990)

window = pygame.display.set_mode(window_dims)
background = (63,63,63)
FPS = 60.0
frame_length = 1/FPS
clock = pygame.time.Clock()

pygame.midi.init()
try:
    player = pygame.midi.Output(0)
except:
    player = pygame.midi.Output(1)
player.set_instrument(0)

#mido.merge_tracks(mid.tracks)

buttons = []
input_boxes = []

def button_funcs(event):
    for button in buttons:
        e = button.handle_event(pygame, event)
        if e != 0:
            if e == 1:
                sys.exit()
            elif e == 2:
                return True
    for button in buttons:
        button.update(pygame.mouse.get_pos())

def input_box_funcs(event):
    for box in input_boxes:
        box.handle_event(pygame, event)
    for box in input_boxes:
        box.update(pygame.mouse.get_pos())

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def lin_map_vel(velocity):
    if velocity == 0:
        return 0
    else:
        return (float(velocity - min_vel)/float(max_vel - min_vel + 1))

def draw_all():
    window.fill(background)
    for note_path in note_paths:
        note_path.update(pygame, window, player)
    pygame.draw.rect(window, background, (0, int(window_dims[1]*5/6), window_dims[0], int(window_dims[1]/6)), 0)
    for note_path in note_paths:
        note_path.draw_piano(pygame, window)

def record_video():
    filename = "Snaps/%04d.png" % file_num
    pygame.image.save(window, filename)
    file_num = file_num + 1

def spawnButton(x, y, w, h, text):
    buttons.append(Button(pygame, int(window_dims[1] / 48), x, y, w, h, (255,255,255), (127,255,127), (127,255,127), text))

def spawnInputBox(x, y, w, h, text):
    input_boxes.append(InputBox(pygame, int(window_dims[1] / 48), x, y, w, h, (255,255,255), (127,255,127), (127,255,127), text))


# OPTION SCREEN

spawnButton(window_dims[0] * 13 / 16 , window_dims[1] * 14 / 16 , window_dims[0] / 8 , window_dims[1] / 16 , "Exit Program")
spawnButton(window_dims[0] * 1 / 16 , window_dims[1] * 14 / 16 , window_dims[0] / 8 , window_dims[1] / 16 , "Start Program")
spawnInputBox(window_dims[0] * 1 / 16 , window_dims[1] * 1 / 16 , window_dims[0] , window_dims[1] / 32 , "Filepath")
spawnInputBox(window_dims[0] * 1 / 16 , window_dims[1] * 2 / 16 , window_dims[0] , window_dims[1] / 32 , "Title")
spawnInputBox(window_dims[0] * 1 / 16 , window_dims[1] * 3 / 16 , window_dims[0] , window_dims[1] / 32 , "Subtitle")
spawnInputBox(window_dims[0] * 1 / 16 , window_dims[1] * 4 / 16 , window_dims[0] , window_dims[1] / 32 , "Composer")
spawnInputBox(window_dims[0] * 1 / 16 , window_dims[1] * 5 / 16 , window_dims[0] , window_dims[1] / 32 , "Arranger")

opt_scr = True

while opt_scr is True:
    pygame.display.flip()
    clock.tick(FPS)
    window.fill(background)
    # Process Events
    for e in pygame.event.get():
        if e.type == KEYUP: # On User Key Press Up
            if e.key == K_ESCAPE: # End Game
                sys.exit()
        if button_funcs(e) is True:
            opt_scr = False
        input_box_funcs(e)
    for button in buttons:
        button.draw(pygame, window)
    for box in input_boxes:
        box.draw(pygame, window)

filepath = input_boxes[0].text

try:
    mid = mido.MidiFile(filepath)
except:
    print("Invalid Filepath")
    filepath = "./examples/midifiles/test.mid"
    mid = mido.MidiFile(filepath)

title = input_boxes[1].text
subtitle = input_boxes[2].text
composer = input_boxes[3].text
arranger = input_boxes[4].text

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

del(opt_scr, buttons, input_boxes)


col1 = hex_to_rgb(args["col1"])
col2 = hex_to_rgb(args["col2"])
i = 0
note_paths = []
while i < 89:
    #i - 1 in NotePath() accounts for NotePath 0 being the path for the pedal
    note_paths.append(NotePath(i - 1, window_dims, int(args["spd"]), col1, col2))
    i += 1
del(i, col1, col2)

# INTRO
font_big = pygame.font.Font("./resources/fonts/SoukouMincho.ttf", int(window_dims[1] / 9))
text_big = font_big.render(title, True, (255, 255, 255))
font_med = pygame.font.Font("./resources/fonts/SoukouMincho.ttf", int(window_dims[1] / 12))
text_med = font_med.render(subtitle, True, (255, 255, 255))
font_sml = pygame.font.Font("./resources/fonts/SoukouMincho.ttf", int(window_dims[1] / 24))
text_sml = font_sml.render("Composed by " + composer + ", Arranged by " + arranger + ".", True, (255,255,255))

del(title, subtitle, composer, arranger)
text_surface = pygame.Surface((window_dims[0], window_dims[1] * 2/3))

#FADE IN
fade_speed = int(frame_length * 180)
alpha = 0
while alpha < 256:
    pygame.display.flip()
    clock.tick(FPS)
    draw_all()
    text_surface.fill((background[0], background[1], background[2], 0))
    text_surface.blit(text_big, (window_dims[0]/2 - text_big.get_width() // 2, \
    window_dims[1]/2 - text_big.get_height() // 2 - window_dims[1]/12))
    text_surface.blit(text_med, (window_dims[0]/2 - text_med.get_width() // 2, \
    window_dims[1]/2 - text_med.get_height() // 2))
    text_surface.blit(text_sml, (window_dims[0]/2 - text_sml.get_width() // 2, \
    window_dims[1]/2 - text_sml.get_height() // 2 + window_dims[1]/16))
    text_surface.set_alpha(alpha)
    window.blit(text_surface, (0,0))
    alpha = alpha + fade_speed
    if is_recording:
        record_video()

#REMAIN
current_time = 0
next_msg_time = float(args["tbs"])
while current_time < next_msg_time:
    pygame.display.flip()
    clock.tick(FPS)
    draw_all()
    window.blit(text_big, (window_dims[0]/2 - text_big.get_width() // 2, \
    window_dims[1]/2 - text_big.get_height() // 2 - window_dims[1]/12))
    window.blit(text_med, (window_dims[0]/2 - text_med.get_width() // 2, \
    window_dims[1]/2 - text_med.get_height() // 2))
    window.blit(text_sml, (window_dims[0]/2 - text_sml.get_width() // 2, \
    window_dims[1]/2 - text_sml.get_height() // 2 + window_dims[1]/16))
    current_time = current_time + frame_length
    if is_recording:
        record_video()

#FADE OUT
alpha = 255
while alpha > 0:
    pygame.display.flip()
    clock.tick(FPS)
    draw_all()
    text_surface.fill((background[0], background[1], background[2], 0))
    text_surface.blit(text_big, (window_dims[0]/2 - text_big.get_width() // 2, \
    window_dims[1]/2 - text_big.get_height() // 2 - window_dims[1]/12))
    text_surface.blit(text_med, (window_dims[0]/2 - text_med.get_width() // 2, \
    window_dims[1]/2 - text_med.get_height() // 2))
    text_surface.blit(text_sml, (window_dims[0]/2 - text_sml.get_width() // 2, \
    window_dims[1]/2 - text_sml.get_height() // 2 + window_dims[1]/16))
    text_surface.set_alpha(alpha)
    window.blit(text_surface, (0,0))
    alpha = alpha - fade_speed
    if is_recording:
        record_video()

#CLEANUP
del(text_big, text_med, text_sml, text_surface, alpha)

#THE MEAT OF THE PROGRAM

mid = mido.MidiFile(filepath)
del(filepath)
iterable = iter(mid)
msg = next(iterable)
next_msg_time = 0
spd = int(args["spd"])
if not live_input:
    current_time = 0
    stop_reading = False
    started_ending = False
    while True:
        try:
            while current_time >= next_msg_time and not stop_reading:
                print(current_time - next_msg_time)
                #print("Pixels to offset: " + str((current_time - next_msg_time) / frame_length * spd))
                print(msg)
                if msg.type == 'note_on' or msg.type == 'note_off':
                    #A0 (note_path[1]) is msg.note == 21
                    note_paths[msg.note + 1 - 21].toggle_note(msg.channel, msg.velocity, \
                    lin_map_vel(msg.velocity), int((current_time - next_msg_time) / frame_length * spd))
                elif msg.is_meta == False:
                    if msg.type == 'control_change':
                        #sustain pedal
                        if msg.control == 64:
                            #if msg.value is 0-63, then pedal (note_path[0]) turns off.
                            #Otherwise, (64-127) turn on.
                            note_paths[0].toggle_note(0, 0, 0, int((current_time - next_msg_time) / frame_length * spd))
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
        except StopIteration:
            #when there are no more messages, trigger a countdown of length tbe\
                next_msg_time = next_msg_time + int(args["tbe"])
                started_ending = True
        finally:
            # Save every frame
            if is_recording:
                record_video()

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
                if current_time >= next_msg_time:
                    print("END")
                    break
else:
    mido.get_input_names()
    port = mido.open_input()
    while True:
        try:
            for msg in port.iter_pending():
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
        except StopIteration:
            #when there are no more messages, trigger a countdown of length tbe\
            started_ending = True
        finally:
            # Save every frame
            if is_recording:
                record_video()

            # Process Events
            for e in pygame.event.get():
                if e.type == KEYUP: # On User Key Press Up
                    if e.key == K_ESCAPE:# End Game
                        sys.exit()


            pygame.display.flip()
            clock.tick(FPS)
            draw_all()

            if started_ending:
                print("END")
                break

# OUTRO

print("Outro")

#FADE TO BLACK

black_screen = pygame.Surface((window_dims[0], window_dims[1]))

alpha = 0
while alpha < 256:
    pygame.display.flip()
    clock.tick(FPS)
    draw_all()
    alpha += fade_speed / 2
    black_screen.set_alpha(alpha)
    window.blit(black_screen, (0,0))
    if is_recording:
        record_video()

#PROCESS VIDEO

if is_recording:
    from subprocess import call
    meth = "python3 tk-img2video.py -d ./images -o ./videos/new_video.mp4 -e jpg -t " + str(FPS)
    call([meth.split()])
