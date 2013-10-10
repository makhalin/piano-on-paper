from mingus.midi import fluidsynth
from mingus.containers.Note import Note
from time import sleep


fluidsynth.init("AI-APiano01trans.sf2")

class Sound:
    "Class for playing piano notes"
    Note_dict = {"C-4":0,"C-5":0,"D-4":0,"D-5":0,"E-4":0,"E-5":0,"F-4":0,
                 "F-5":0,"G-4":0,"G-5":0,"A-4":0,"A-5":0,"B-4":0,"B-5":0}
            
    def press_key(self,note):
        #if self.Note_dict[note] == 0:
        print note
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


'''from Tkinter import *

root = Tk()
S = Sound()

update_array = ["F-5"]
S.update(update_array)
S.press_key('F-5')
def note1(*ignore):
    S.press_key("C-4")
def note2(*ignore):
    S.press_key("D-4")
def note3(*ignore):
    S.press_key("E-4")
def note4(*ignore):
    S.press_key("C-5")
def note5(*ignore):
    S.press_key("D-5")

root.bind('<a>', note1)
root.bind('<d>', note2)
root.bind('<k>', note3)
root.bind('<l>', note4)
root.bind('<s>', note5)
root.mainloop() '''
