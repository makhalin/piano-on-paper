from mingus.midi import fluidsynth
from mingus.containers.Note import Note


fluidsynth.init("./resources/s1.sf2", "jck")
fluidsynth.play_Note(Note('A-3'))











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

