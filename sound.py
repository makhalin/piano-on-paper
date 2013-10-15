import cv2
from mingus.midi import fluidsynth
from mingus.containers.Note import Note
from pprint import pprint


class SoundPlayer:
    "Class for playing piano notes"
    def __init__(self, filename):
        fluidsynth.init(filename)
        note_names = ("C-4", "C#4", "D-4", "D#4", "E-4", "F-4", "F#4", "G-4", "G#4", "A-4", "A#4", "B-4",
                      "C-5", "C#5", "D-5", "D#5", "E-5", "F-5", "F#5", "G-5", "G#5", "A-5", "A#5", "B-5")
        coords = (15, 35, 52, 71, 88, 125, 144, 160, 180, 197, 216, 234, 
                  270, 289, 307, 325, 343, 378, 398, 415, 434, 452, 470, 487)
        
        self.is_pressed = dict.fromkeys(note_names, [False] * len(note_names))
        self.note_coordinate = dict(zip(note_names, coords))
        self.note_names = note_names

        self.window_title = 'Keyboard'
        cv2.namedWindow(self.window_title)
        self.img = cv2.imread('./resources/keyboard.jpg', cv2.CV_LOAD_IMAGE_COLOR)
        cv2.imshow(self.window_title, self.img)
        self.turn_sound_on()


    def press_key(self, note):
        if self.is_sound_on:
            fluidsynth.play_Note(Note(note))


    def play_notes(self, notes_to_play):
        for note in notes_to_play:
            if not self.is_pressed[note]:
                self.press_key(note)
        for note in self.note_names:
            self.is_pressed[note] = note in notes_to_play
        self.draw_piano()


    def draw_piano(self):
        white = (255, 255, 255)
        red = (0, 0, 255)
        black = (0, 0, 0)
        for note in self.is_pressed:
            color = red if self.is_pressed[note] else white
            if note[1:2] == '-':
                cv2.circle(self.img, (self.note_coordinate[note], 210), 10, color, -1)
            else:
                color = red if self.is_pressed[note] else black
                cv2.circle(self.img, (self.note_coordinate[note], 110), 10, color, -1)

        cv2.imshow(self.window_title, self.img)

    def turn_sound_on(self):
        self.is_sound_on = True

    def turn_sound_off(self):
        self.is_sound_on = False
       
        
