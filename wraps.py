from math import sin, cos, sqrt, pi
import cv2
import cv2.cv as cv
import numpy as np


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, p):
        dx = self.x - p.x
        dy = self.y - p.y
        return sqrt(dx ** 2 + dy ** 2)

    def get_coords(self):
        return (self.x, self.y)


class Contour(object):
    def __init__(self, cnt):
        self.contour = cnt

        self.area = self.get_area()
        self.perimeter = self.get_perimeter()
        self.center = self.get_centroid()


    @staticmethod
    def from_points(points):
        cnt = np.array([[p.get_coords() for p in points]], dtype=np.int32)
        return Contour(cnt)


    def get_area(self):
        return float(cv2.contourArea(self.contour))


    def get_perimeter(self):
        return float(cv2.arcLength(self.contour, closed=True))


    def get_centroid(self):
        M = cv2.moments(self.contour)
        if abs(M['m00']) > 0.05:
            centroid_x = int(M['m10'] / M['m00'])
            centroid_y = int(M['m01'] / M['m00'])
            return Point(centroid_x, centroid_y)
        else:
            return None


    def distance_to(self, cnt):
        return self.center.distance_to(cnt.center)


    def get_bounding_rectangle(self):
        return cv2.boundingRect(self.contour)


    def get_defect(self, cnt):
        return cv2.matchShapes(self.contour, cnt.contour, cv.CV_CONTOURS_MATCH_I2, -1)


    def draw(self, image, color):  # draws a contour on given image
        cv2.drawContours(image.image, [self.contour], -1, color, 6)


    def fill(self, img, color):  # draws a filled contour
        cv2.drawContours(img, [self.contour], -1, color, -1)


    def make_convex(self):
        return Contour(cv2.convexHull(self.contour))


    def to_points(self):  # TODO: change this. [[[1]], [[2]], ..., [[n]]] -> [[1], [2], ..., [n]]
        #return [np.array(p[0]) for p in self.contour]
        return [Point(*p[0]) for p in self.contour]


    def approximate(self, gap):  # selfapproximation
        self.contour = cv2.approxPolyDP(self.contour, gap, True)


    def is_ellipse(self):  # heuristic ellipse detection
        if not 250 < self.area < 3000:
            return False

        x, y, w, h = self.get_bounding_rectangle()
        a = float(w) / 2
        b = float(h) / 2

        if not 0.5 < a/b < 3:
            return False

        expected_area = pi * a * b
        expected_perimeter = pi * (3 * (a + b) - sqrt((3 * a + b) * (3 * b + a)))

        if 0.85 < self.area / expected_area < 1.05:
            if 0.95 < self.perimeter / expected_perimeter < 1.1:
                return True

        return False


    def __len__(self):
        return len(self.contour)


class Image(object):
    def __init__(self, image):
        super(Image, self).__init__()
        self.image = image
    

    def copy(self):
        return Image(self.image.copy)

    
    def show(self, window_name):
        cv2.imshow(window_name, self.image)


    def to_gray(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return Image(gray)


    def get_treshold(self, thresh=127, maxval=255, threshold_type=cv2.THRESH_BINARY):
        ret, thresh = cv2.threshold(self.image, thresh, maxval, threshold_type)
        return Image(thresh)


    def find_contours(self):
        contours, h = cv2.findContours(self.image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        #contours, h = cv2.findContours(self.image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return [Contour(cnt) for cnt in contours]
  
    def perspective(self, src_points, dest_points, res_size):
        src_points = np.array([p.get_coords() for p in src_points], np.float32)
        dest_points = np.array([p.get_coords() for p in dest_points], np.float32)
        T = cv2.getPerspectiveTransform(src_points, dest_points)
        result = cv2.warpPerspective(self.image, T, res_size)
        return Image(result)

    def eroded(self, kernel_size=(2, 2)):
        kernel = np.ones(kernel_size,'uint8')
        return Image(cv2.erode(self.image, kernel))

    def dilated(self, kernel_size=(2, 2)):
        kernel = np.ones(kernel_size,'uint8')
        return Image(cv2.dilate(self.image, kernel))