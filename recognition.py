from itertools import combinations
from wraps import Image, Contour, Point
from math import sqrt


class KeyboardRecognizer(object):
    """ Recognizes the keyboard image using its topology """
    def __init__(self, frame):
        super(KeyboardRecognizer, self).__init__()
        self.image = Image(frame)

        proportions = reversed([(3./16, 7./16),
                       (6./16, 3./16),
                       (10./16, 3./16),
                       (13./16, 7./16)])
        width = 400
        height = int(400 / sqrt(2))
        self.elatole_size = (width, height)

        self.etalone_orients = [Point(width * px, height * py)
                                    for px, py in proportions]



    def get_all_ellipses(self):
        gray = self.image.to_gray()
        thresh = gray.get_treshold()
        contours = thresh.find_contours()
        ellipses = [cnt for cnt in contours if cnt.is_ellipse()]
        return ellipses


    def choose_four(self, ellipses):
        if len(ellipses) < 4:
            return None

        candidates = []
        for four in combinations(ellipses, 4):
            centers = [e.center for e in four]
            cnt = Contour.from_points(centers)
            cnt = cnt.make_convex()
            if len(cnt) != 4:
                continue

            centers = cnt.to_points()
            centers = sorted(centers, key=lambda p:p.x)
            
            areas = [e.get_area() for e in four]
            diff = max(areas) - min(areas)

            candidates.append((diff, centers))

        centers = min(candidates, key=lambda x:x[0])[1]
        return centers


    def transformed(self):
        ''' Returns the tranformed image'''
        ellipses = self.get_all_ellipses()
        for e in ellipses:
            e.draw(self.image, color=(255, 60, 60))

        orients = self.choose_four(ellipses)
        if orients is not None:
            cnt = Contour.from_points(orients)
            cnt.draw(self.image, color=(60, 60, 255))

            corrected_image = self.image.perspective(orients,
                                                     self.etalone_orients,
                                                     self.elatole_size)
            return corrected_image
        return None


    def get_keyboard(self):
        transformed_image = self.transformed()
        if transformed_image is not None:
            gray = transformed_image.to_gray()
            gray = gray.eroded((3, 3))
            return gray

        return None



class KeysRecognizer(object):
    def __init__(self, keyboard_image):
        self.image = keyboard_image
        self.image.show('keyboard')

    def get_pressed_keys(self):
        tresh = self.image.get_treshold(140, 255)
        tresh.show('keyboard')
        contours = tresh.find_contours()
        