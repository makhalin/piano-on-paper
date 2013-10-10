
class SoundPlayer:
    "Class imitating piano playing"
    def __init__(self, init_filename):
        self.notes = []
        self.is_playing = dict()
        self.keys = []
        for note in ('C', 'D', 'E', 'F', 'G', 'A', 'B'):
            self.notes.append(note + '-4')
            self.notes.append(note + '-5')
        for note in self.notes:
            self.is_playing[note] = False

        #cv2.imshow('VirtualKeyboard', vk)

    def press_key(self, note):
        self.is_playing[note] = True
        print('Pressed %s' % note)

    def release_key(self, note):
        self.is_playing[note] = False
        print('Released %s' % note)

    def play_notes(self, notes_to_play):
        print(notes_to_play)
