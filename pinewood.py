#!/usr/bin/env python3
from tkinter import *
from tkinter import * 
import pyglet
import os
import time
import datetime
import RPi.GPIO as GPIO

# Prerequisites:
# Install font ds_digital.ttf
# sudo apt install python3-pyglet

GPIO.setmode(GPIO.BCM)
#GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(25, GPIO.IN)

root_window_widget = Tk()
root_window_widget.title('Pinewood Derby')
root_window_widget.attributes('-fullscreen', True)
root_icon_photo_image = PhotoImage(file = 'pinewood_200_public_domain.png')
root_window_widget.iconphoto(True, root_icon_photo_image)

Grid.columnconfigure(root_window_widget, 0, weight=1)
Grid.columnconfigure(root_window_widget, 1, weight=1)
Grid.columnconfigure(root_window_widget, 2, weight=1)
Grid.columnconfigure(root_window_widget, 3, weight=1)

track_0_elapsed_time = 0
track_1_elapsed_time = 0
track_2_elapsed_time = 0
track_3_elapsed_time = 0
gate_time = time.time()
next_finishing_place = 1

time_label_0 = Label(root_window_widget)
time_label_1 = Label(root_window_widget)
time_label_2 = Label(root_window_widget)
time_label_3 = Label(root_window_widget)
time_label_0.grid(row = 0, column = 0, sticky = EW)
time_label_1.grid(row = 0, column = 1, sticky = EW)
time_label_2.grid(row = 0, column = 2, sticky = EW)
time_label_3.grid(row = 0, column = 3, sticky = EW)
time_label_0['fg'] = '#FF0000'
time_label_1['fg'] = '#FF0000'
time_label_2['fg'] = '#FF0000'
time_label_3['fg'] = '#FF0000'
time_label_0['bg'] = '#000000'
time_label_1['bg'] = '#000000'
time_label_2['bg'] = '#000000'
time_label_3['bg'] = '#000000'
time_label_0['font'] = ('DS-Digital', 144)
time_label_1['font'] = ('DS-Digital', 144)
time_label_2['font'] = ('DS-Digital', 144)
time_label_3['font'] = ('DS-Digital', 144)
time_label_0['padx'] = 50
time_label_1['padx'] = 50
time_label_2['padx'] = 50
time_label_3['padx'] = 50


place_label_0 = Label(root_window_widget)
place_label_1 = Label(root_window_widget)
place_label_2 = Label(root_window_widget)
place_label_3 = Label(root_window_widget)
place_label_0.grid(row = 1, column = 0, sticky = EW)
place_label_1.grid(row = 1, column = 1, sticky = EW)
place_label_2.grid(row = 1, column = 2, sticky = EW)
place_label_3.grid(row = 1, column = 3, sticky = EW)
place_label_0['font'] = ('DS-Digital', 300)
place_label_1['font'] = ('DS-Digital', 300)
place_label_2['font'] = ('DS-Digital', 300)
place_label_3['font'] = ('DS-Digital', 300)
place_label_0['fg'] = '#00FF00'
place_label_1['fg'] = '#00FF00'
place_label_2['fg'] = '#00FF00'
place_label_3['fg'] = '#00FF00'
place_label_0['bg'] = '#505050'
place_label_1['bg'] = '#505050'
place_label_2['bg'] = '#505050'
place_label_3['bg'] = '#505050'

finish_button_0 = Button(root_window_widget)
finish_button_1 = Button(root_window_widget)
finish_button_2 = Button(root_window_widget)
finish_button_3 = Button(root_window_widget)
finish_button_0['text'] = 'Finish 0'
finish_button_1['text'] = 'Finish 1'
finish_button_2['text'] = 'Finish 2'
finish_button_3['text'] = 'Finish 3'
finish_button_0.grid(row = 2, column = 0)
finish_button_1.grid(row = 2, column = 1)
finish_button_2.grid(row = 2, column = 2)
finish_button_3.grid(row = 2, column = 3)

reset_and_start_button = Button(root_window_widget)
reset_and_start_button['text'] = 'Reset and Start'
reset_and_start_button['padx'] = 10
reset_and_start_button['pady'] = 10
reset_and_start_button.grid(row = 3, column = 0, columnspan = 4)

gate_time_label = Label(root_window_widget)
gate_time_label.grid(row = 4, column = 0, columnspan = 4)
gate_time_label['bg'] = '#000000'
gate_time_label['fg'] = '#FFFF00'
gate_time_label['font'] = ('DS-Digital', 12)
gate_time_label['padx'] = 10



def reset_and_start_race():
	global gate_time, next_finishing_place, track_reset_time
	global track_0_elapsed_time, track_1_elapsed_time, track_2_elapsed_time, track_3_elapsed_time
	gate_time = time.time()
	track_0_elapsed_time = 0
	track_1_elapsed_time = 0
	track_2_elapsed_time = 0
	track_3_elapsed_time = 0
	next_finishing_place = 1
	time_label_0['text'] = "0.000"
	time_label_1['text'] = "0.000"
	time_label_2['text'] = "0.000"
	time_label_3['text'] = "0.000"
	finish_button_0['state'] = "normal"
	finish_button_1['state'] = "normal"
	finish_button_2['state'] = "normal"
	finish_button_3['state'] = "normal"
	place_label_0['text'] = ''
	place_label_1['text'] = ''
	place_label_2['text'] = ''
	place_label_3['text'] = ''
	gate_time_label['text'] = datetime.datetime.fromtimestamp(gate_time).strftime("%Y-%m-%d %H:%M:%S.%f")

reset_and_start_race()

def finish0(channel):
	global track_0_elapsed_time, next_finishing_place
	if track_0_elapsed_time == 0:
		track_0_elapsed_time = time.time() - gate_time
		time_label_0['text'] = "{:15.3f}".format(track_0_elapsed_time).strip()
		place_label_0['text'] = next_finishing_place
		next_finishing_place = next_finishing_place + 1

def finish1(channel):
	global track_1_elapsed_time, next_finishing_place
	if track_1_elapsed_time == 0:
		track_1_elapsed_time = time.time() - gate_time
		time_label_1['text'] = "{:15.3f}".format(track_1_elapsed_time).strip()
		place_label_1['text'] = next_finishing_place
		next_finishing_place = next_finishing_place + 1

def finish2(channel):
	global track_2_elapsed_time, next_finishing_place
	if track_2_elapsed_time == 0:
		track_2_elapsed_time = time.time() - gate_time
		time_label_2['text'] = "{:15.3f}".format(track_2_elapsed_time).strip()
		place_label_2['text'] = next_finishing_place
		next_finishing_place = next_finishing_place + 1

def finish3(channel):
	global track_3_elapsed_time, next_finishing_place
	if track_3_elapsed_time == 0:
		track_3_elapsed_time = time.time() - gate_time
		time_label_3['text'] = "{:15.3f}".format(track_3_elapsed_time).strip()
		place_label_3['text'] = next_finishing_place
		next_finishing_place = next_finishing_place + 1

finish_button_0['command'] = finish0(0)
finish_button_1['command'] = finish1(0)
finish_button_2['command'] = finish2(0)
finish_button_3['command'] = finish3(0)
reset_and_start_button['command'] = reset_and_start_race

def starting_gate_callback(channel):
	global reset_and_start_race, gate_time
	if time.time() - gate_time > 1:
		print("Gate event honored")
		reset_and_start_race()
	else:
		print('.')
	gate_time = time.time()

GPIO.add_event_detect(26, GPIO.BOTH, callback=starting_gate_callback)
GPIO.add_event_detect(22, GPIO.BOTH, callback=finish0)
GPIO.add_event_detect(23, GPIO.BOTH, callback=finish1)
GPIO.add_event_detect(24, GPIO.BOTH, callback=finish2)
GPIO.add_event_detect(25, GPIO.BOTH, callback=finish3)


root_window_widget.mainloop()

