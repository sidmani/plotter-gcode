import numpy as np


# invert the Y axis
def correct_svg_bbox(bbox):
    return np.array([bbox[0], bbox[3], bbox[2], bbox[1]])


# create the transform between the SVG coordinates and the printer coordinates
def make_transform(frame_A, frame_B):
    A = np.array([[frame_A[2] - frame_A[0], 0], [0, frame_A[3] - frame_A[1]]])
    B = np.array([[frame_B[2] - frame_B[0], 0], [0, frame_B[3] - frame_B[1]]])
    scale = np.matmul(np.linalg.inv(A), B)

    A_origin = np.array([frame_A[0], frame_A[1]])
    B_origin = np.array([frame_B[0], frame_B[1]])
    offset = B_origin - (scale @ A_origin)
    return scale, offset


def apply_transform(point, scale, offset):
    return scale @ np.array([*point]) + offset
