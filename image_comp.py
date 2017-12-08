"""
image_comp

Calculates differences between images using OpenCV and numpy

Nicholas Bochenski & Franciszek Madej
"""

import cv2
import numpy as np


def magn(v):
    """Returns length of vector"""
    return np.sum(v**2)**.5


def dist(a, b):
    """Return distance between two points"""
    return magn(a-b)


def lerp(a, b, t):
    """Linear interpolation"""
    return a + (b-a) * np.stack([t, t], axis=-1)


def line(a, b):
    """Returns set of points from line"""
    distance = dist(a, b)
    point_set = np.arange(0, distance + 1)
    return lerp(a, b, point_set / distance)


def color_at(img, pos):
    """Returns color at given position"""
    try:
        return img[int(pos[1])][int(pos[0])]
    except:  # noqa
        return img[0][0]


def color_line(img, a, b):
    """Returns line of colors (point set)"""
    return [color_at(img, pos) for pos in line(a, b)]


def variance(img, a, b):
    """Self describing!"""
    line = color_line(img, a, b)
    avg = np.average(line)
    return np.sum((line - avg)**2)


def img_size(img):
    """Returns OpenCV image size"""
    return np.array([len(img[0]), len(img)])


def img_center(img):
    """Returns image center"""
    return img_size(img) / 2


def perpendicular_pos(pos):
    """Given point (x, y) return (-y, x)"""
    return np.array([-pos[1], pos[0]])


def perpendicular(img, a, b):
    """
    Calculates and returns points in perpendicular position to the point
    provided
    """
    center = img_center(img)
    a_recentered = a - center
    b_recentered = b - center
    return (perpendicular_pos(a_recentered) + center,
            perpendicular_pos(b_recentered) + center)


def angle_line(img, theta):
    """
    Calculates points for line given the theta (tg(theta) = a in a*x + b =0)
    """
    a_norm = np.array([np.cos(theta), np.sin(theta)])
    radius = img_size(img)[0] / 2
    a = a_norm * radius + img_center(img)
    b = -a_norm * radius + img_center(img)
    return a, b


def min_variance(img):
    """
    Calculates minimal variance for a given image
    """
    min_var = float('inf')
    result = (0, 0)
    for theta in np.arange(0, 2 * np.pi, 0.01):
        a, b = angle_line(img, theta)
        var = variance(img, a, b)
        if var < min_var:
            min_var = var
            result = (a, b)
    return result[0], result[1]


def draw(img, point_set):
    """
    Draws point set on image
    """
    result = img.copy()
    for point in point_set:
        result[int(point[1])][int(point[0])] = 0
    return result


def load_img(fname):
    """
    Loads image in greyscale
    """
    return cv2.imread(fname, cv2.IMREAD_GRAYSCALE)


def preview(img):
    """
    Spawns window to preview changes
    """
    cv2.imshow('img', img)
    cv2.waitKey(100000)
    cv2.waitKey(100000)
    cv2.destroyWindow('img')
