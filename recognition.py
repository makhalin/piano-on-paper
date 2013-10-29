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
        gray = self.image.to_gray()
        ellipses = [e for e in ellipses if gray.get_pixel(e.center.reversed()) < 100]  # with dark enters only
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
            transformed_image = fix_channels(transformed_image)
            gray = transformed_image.to_gray()
            gray = gray.eroded((3, 3))

            height, width = gray.get_size()
            recog_height = int(0.6 * height)
            return Image(gray.image[recog_height:, :])

        return None


def fix_channels(image):
    (R, G, B) = image.split()
    return Image.from_channels([R, G, R])



class KeysRecognizer(object):
    def __init__(self, keyboard_image, window_title):
        self.image = keyboard_image
        self.window_title = window_title

        height, width = self.image.get_size()
        control_points = [Point(8 * height // 9,  ((2 * i + 1) * width) // 28) for i in range(14)]
        note_names = ("C-4", "D-4", "E-4", "F-4", "G-4", "A-4", "B-4", "C-5", "D-5", "E-5", "F-5", "G-5", "A-5", "B-5")
        self.points = dict(zip(control_points, note_names))
        

    def get_pressed_keys(self):
        tresh = self.image.get_treshold(90, 255)
        pressed_keys = []

        black = 0
        means = []
        delta = Point(12, 9)

        for point in self.points:
            tresh.draw_circle(point, radius=7, color=128)

            tl = point - delta
            br = point + delta
            
            mean = tresh.get_mean_color_in_rect(tl, br)
            tresh.draw_rectangle(tl, br, 0)
            #if tresh.get_pixel(point) == black:
            print(int(mean))
            if mean < 120:
                pressed_keys.append(self.points[point])

        tresh.show(self.window_title)

        return pressed_keys


