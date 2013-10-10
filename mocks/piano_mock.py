import cv2
from cv2 import cv
import recognition_mock as recognition
from time import time
from sound import Sound

def main():
    cv.NamedWindow("original", cv.CV_WINDOW_AUTOSIZE)

    cam = cv2.VideoCapture(0)
    cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, 10)
    cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 10)
    cam.set(cv.CV_CAP_PROP_FPS, 24)

    s = Sound()
    ret, frame = cam.read()
    while True:
        ret, frame = cam.read()

        r = recognition.Recognizer(frame)
        notes = r.get_notes()
        s.update(notes)

        if cv2.waitKey(1) == 27:  # Escape code
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
