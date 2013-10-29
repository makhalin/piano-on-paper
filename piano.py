import cv2
from cv2 import cv
from recognition import KeyboardRecognizer, KeysRecognizer
import sound as sound


def main():
    cv.NamedWindow("original", cv.CV_WINDOW_AUTOSIZE)
    cv.NamedWindow("keyboard", cv.CV_WINDOW_AUTOSIZE)

    cam = cv2.VideoCapture(0)
    cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, 600)
    cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
    cam.set(cv.CV_CAP_PROP_FPS, 24)
    ret, frame = cam.read()

    player = sound.SoundPlayer('./resources/s1.sf2')
    #player.turn_sound_off();

    while True:
        ret, frame = cam.read()

        keyboard_image = KeyboardRecognizer(frame).get_keyboard()
        if keyboard_image is not None:
            notes = KeysRecognizer(keyboard_image, 'keyboard').get_pressed_keys()
            player.play_notes(notes)

        cv2.imshow('original', frame)
        
        if cv2.waitKey(1) == 27:  # Escape code
            break

    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()
