from itertools import combinations
from wraps import Image, Contour, Point
from math import sqrt

class Recognizer(object):
    """ Recognizes the keyboard image using its topology """
    def __init__(self, frame):
        super(Recognizer, self).__init__()
        self.image = Image(frame)

        proportions = ((3./16, 7./16),
                       (6./16, 3./16),
                       (10./16, 3./16),
                       (13./16, 7./16))
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


    def recognize(self):
        ''' Returns the tranformation matrix'''
        ellipses = self.get_all_ellipses()
        if len(ellipses) == 2:
            return []
        elif len(ellipses) == 1:
            C = ellipses[0]            
            if C.get_centroid().x < self.image.image.shape[0] / 2:
                return ['C-4']
            else:
                return ['F-5']
        else:
            return ['C-4', 'F-5']


    def get_notes(self):
        return self.recognize()

