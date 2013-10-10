import cv2
from cv2 import cv
import recognition
import mocks.sound_mock as sound



def main():
    cv.NamedWindow("original", cv.CV_WINDOW_AUTOSIZE)
    cv.NamedWindow("keyboard", cv.CV_WINDOW_AUTOSIZE)

    cam = cv2.VideoCapture(0)
    cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, 600)
    cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
    cam.set(cv.CV_CAP_PROP_FPS, 24)

    player = sound.SoundPlayer('./resources/s1.sf2')

    ret, frame = cam.read()
    while True:
        ret, frame = cam.read()

        keyboard_recog = recognition.KeyboardRecognizer(frame)
        keyboard_image = keyboard_recog.get_keyboard()
        if keyboard_image is not None:
            keys_recog = recognition.KeysRecognizer(keyboard_image)
            notes = keys_recog.get_pressed_keys()
            player.play_notes(notes)

        cv2.imshow('original', frame)
        
        if cv2.waitKey(1) == 27:  # Escape code
            break

    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()
