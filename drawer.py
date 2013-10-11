import cv2
import numpy as np
from math import sqrt


size = 12
upper_gap = 30
bottom_gap = 10
gap = 10
white_key_height = 40 * size
white_key_width = 10 * size
black_key_height = 24 * size
black_key_width = 2 * size + gap + 4 * size

height = upper_gap + white_key_height + bottom_gap
width = gap + 14 * (white_key_width + gap)

white = 255
black = 0

img = np.zeros((height, width), np.uint8)


fout = open('./resources/topology.txt', 'w')


def set_rect(x, y, dx, dy, color):
    cv2.rectangle(img, (x, y), (x + dx, y + dy), color, -1)
    fout.write('%d %d %d %d\n' % (x, y, x + dx, y + dy))


# WHITE KEYS

fout.write('whites:\n')
x, y = (gap, upper_gap)
dx = white_key_width
dy = white_key_height
for i in range(14):
    set_rect(x, y, dx, dy, white)
    x += white_key_width + gap


# BLACK KEYS

fout.write('blacks:\n')

dx = black_key_width
dy = black_key_height

x = gap + 6 * size
y = upper_gap
set_rect(x, y, dx, dy, black)

x += black_key_width + 6 * size
set_rect(x, y, dx, dy, black)

x += black_key_width + 6 * size + gap + 6 * size
set_rect(x, y, dx, dy, black)

x += black_key_width + 5 * size
set_rect(x, y, dx, dy, black)

x += black_key_width + 5 * size
set_rect(x, y, dx, dy, black)

x += black_key_width + 6 * size + gap + 6 * size
set_rect(x, y, dx, dy, black)

x += black_key_width + 6 * size
set_rect(x, y, dx, dy, black)

x += black_key_width + 6 * size + gap + 6 * size
set_rect(x, y, dx, dy, black)

x += black_key_width + 5 * size
set_rect(x, y, dx, dy, black)

x += black_key_width + 5 * size
set_rect(x, y, dx, dy, black)

x += black_key_width + 6 * size



# RECOGNITION PART


recog_width = width
recog_height = int(width / sqrt(2)) - height

recog_img = np.empty((recog_height, recog_width), np.uint8)
recog_img.fill(white)


radius = width // 20
abs_height = height + recog_height
abs_width = width

# width / height
proportions = ((3./16, 7./16),
			   (6./16, 3./16),
			   (10./16, 3./16),
			   (13./16, 7./16))


for p_x, p_y in proportions:
    center = (int(abs_width * p_x),
    	      int(abs_height * p_y))
    cv2.circle(recog_img, center, radius, black, -1)


# SUMMARY

result = np.empty((height + recog_height, width), np.uint8)
result[:recog_height, :] = recog_img
result[-height:, :] = img


cv2.imwrite('./resources/kb.jpg', result)