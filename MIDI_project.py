import mido
import pygame
# Get key commands for input
from pygame.locals import *
# sys module for terminating process
# Should replace end game with something like pygame.endgame or something
import sys
pathToMidi = "./bumble_bee.mid"
# from note_object import NoteObj
import time
from datetime import datetime, date

class NoteTrack():
    #this file holds the note_track class
    def __init__(self, number):
        self.x = number * 20
        self.y = 0
        self.notes = []
        
    def start_note(self, channel, velocity):
        self.notes.append(NoteObj(self.x, channel, velocity))
        
    def stop_note(self):
        self.notes[-1].stop_growing()
        
    def update(self):
        for n, i in enumerate(self.notes):
            i.draw()
            i.move()
            if i.y >= surface_dims[1]:
                del(self.notes[n])

class NoteObj():
    # this file holds the note class 
    def __init__(self, x, channel, velocity):
        self.height = 20
        self.width = 20
        self.x = x
        self.y = 10
        self.change_x = 0
        self.change_y = 5
        self.color = (0,0,128)
        self.thickness = 0
        self.is_still_on = True
        
    def stop_growing(self):
        self.is_still_on = False
        
    def move(self):
        self.x += self.change_x
        
        if self.is_still_on:
            self.height += self.change_y
        else: 
            self.y += self.change_y
        
    def draw(self):
        #print("drawing " + str(self.x) + " " + str(self.y))
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), self.thickness)

pygame.init()
pygame.display.set_caption('MIDI Project')
surface_dims = (1760, 990)
surface = pygame.display.set_mode(surface_dims)
background = (255,255,255)
FPS = 60
clock = pygame.time.Clock()

mid = mido.MidiFile(pathToMidi)
note_tracks = []
i = 0
j = 0

start_time = time.time()
next_spawn_time = start_time

mido.merge_tracks(mid.tracks)

iterable = iter(mid)
msg = next(iterable) 

while j < 88:
    note_tracks.append(NoteTrack(j))
    j += 1
    # print("spawn" + str(j))

# parse MIDI file and spawn notes in actual time
# for msg in mid.play(meta_messages=True): changed
# draw & update notes\

while True:
    surface.fill(background)
    for note_track in note_tracks:
        note_track.update()
    try:
         
        while time.time() >= next_spawn_time:
            print(msg)
            if msg.type == 'note_on' and msg.velocity != 0:
                note_tracks[msg.note - 21].start_note(msg.channel, msg.velocity)
            elif msg.type == 'note_on' and msg.velocity == 0:
                note_tracks[msg.note - 21].stop_note()
                print("ending")
            else:
                pass

                
            msg = next(iterable)
            next_spawn_time = next_spawn_time + msg.time 
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

        

# for msg in mid:
    
#     print(msg)

#     if msg.type == 'note_on':
#         note_tracks[msg.note - 21].start_note(msg.channel, msg.velocity)
    
#     elif msg.type == 'note_off':
#         note_tracks[msg.note - 21].stop_note()
        
#     elif msg.is_meta == False:
#         pass
#     else:
#         #is metaMessage
        
#         #attrs = vars(msg)
#         #print(attrs)
#         if msg.type == 'text':
#             pass
#         elif msg.type == 'copyright':
#             pass
#         elif msg.type == 'set_tempo':
#             pass
#         elif msg.type == 'time_signature':
#             pass
#         elif msg.type == 'end_of_track':
#             pass
#         else:
#             pass
