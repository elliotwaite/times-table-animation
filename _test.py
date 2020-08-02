import glob
import math
import multiprocessing as mp
import os
import shutil
import subprocess

import cairo
import numpy as np
import tqdm

WIDTH = 1920 * 2
HEIGHT = 1080 * 2

DTYPE = np.float64
MIN_DELTA = np.finfo(DTYPE).eps * 1e3
LINE_EXTENSION_LENGTH = np.array(WIDTH * 3 / 4, dtype=DTYPE)

CENTER = np.array([WIDTH / 2, HEIGHT / 2], dtype=DTYPE)
RADIUS = np.array(HEIGHT / 2, dtype=DTYPE)
TAU = np.array(np.pi * 2, dtype=DTYPE)
TAU_OVER_4 = np.array(np.pi / 2, dtype=DTYPE)

LINE_WIDTH = 16
# OPERATOR_MODE = cairo.Operator.SCREEN
OPERATOR_MODE = cairo.Operator.OVERLAY

# FPS = 60

NUM_DOTS = np.array(4, dtype=DTYPE)
DOTS_MULTIPLE = np.array(3, dtype=DTYPE)


def main():
    multiple = 3
    print('start dot indexes:', np.arange(int(NUM_DOTS)))
    print('end dot indexes:', np.arange(int(NUM_DOTS)) * multiple % NUM_DOTS)

    start_fractions = np.arange(int(NUM_DOTS), dtype=DTYPE) / NUM_DOTS
    start_angles = start_fractions * TAU
    print('start_angles:', start_angles)

    delta_angles = (start_angles * multiple - start_angles) % TAU
    delta_angles = np.clip(delta_angles, MIN_DELTA, None)
    print('delta_angles:', delta_angles)

    start_angles -= TAU_OVER_4

    end_angles = start_angles + delta_angles
    print('end_angles:', end_angles)

    start_points = CENTER + RADIUS * np.stack([np.cos(start_angles), np.sin(start_angles)], axis=1)
    end_points = CENTER + RADIUS * np.stack([np.cos(end_angles), np.sin(end_angles)], axis=1)

    diffs = end_points - start_points
    print('diffs:', diffs)
    print('diff norms:', np.linalg.norm(diffs, axis=1))

    unit_diffs = diffs / np.linalg.norm(diffs, axis=1)[..., None]
    print('unit_diffs:', unit_diffs)

    start_points -= unit_diffs * LINE_EXTENSION_LENGTH
    end_points += unit_diffs * LINE_EXTENSION_LENGTH
    print('start_points:', start_points)
    print('end_points:', end_points)


if __name__ == '__main__':
    main()
