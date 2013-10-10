import cv2
from mingus.midi import fluidsynth
from mingus.containers.Note import Note
from time import sleep

class Sound:
    "Class for playing piano notes"

    def init(self, filename):
        fluidsynth.init(filename)
        Note_dict = {"C-4" : 0, "C-5" : 0, "D-4" : 0, "D-5" : 0, "E-4" : 0, "E-5" : 0, "F-4" : 0,
                 "F-5" : 0, "G-4" : 0, "G-5" : 0, "A-4" : 0, "A-5" : 0, "B-4" : 0, "B-5" : 0}
        Note_point_x = {"C-4" : 15, "D-4" : 52, "E-4" : 88, "F-4" : 125, "G-4" : 160, "A-4" : 197,
                    "B-4" : 234, "C-5" : 270, "D-5" : 307, "E-5" : 343, "F-5" : 378, "G-5" : 415, "A-5" : 452, "B-5" : 487}
        img = cv2.imread('keyboard.jpg',cv2.CV_LOAD_IMAGE_COLOR)
        cv2.namedWindow('Display Window')
        cv2.imshow('Display Window',img)
            
    def press_key(self,note):
        #if self.Note_dict[note] == 0:
        # print note
        fluidsynth.play_Note(Note(note))
        
    def release_key(self,note):
        self.Note_dict[note] = 0

    def update(self, update_array):
        update_dict = {}
        update_dict = self.Note_dict.copy()
        for note in update_dict :
            update_dict[note] = 0
        for note in update_array:
            update_dict[note] = 1
        for note in self.Note_dict :
            if self.Note_dict[note] != update_dict[note] :
                if update_dict[note] == 1:
                    self.press_key(note)
        self.Note_dict = update_dict
        self.draw_piano()

    def draw_piano(self):
        for note in self.Note_dict :
            if self.Note_dict[note] == 1 :
                cv2.circle(self.img, (self.Note_point_x[note], 210), 10, (0,0,255), -1)
            else :
                cv2.circle(self.img, (self.Note_point_x[note], 210), 10, (255,255,255), -1)

        cv2.imshow('Display Window',self.img)

        
        
