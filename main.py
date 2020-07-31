import multiprocessing as mp
import os
import shutil

import cairo
import numpy as np
import tqdm

CUR_DIR = os.path.join(os.path.dirname(__file__))
FRAMES_DIR = os.path.join(CUR_DIR, 'frames')
OUTPUT_PATH = os.path.join(CUR_DIR, 'movie.mov')

WIDTH = 1920 * 2
HEIGHT = 1080 * 2

DTYPE = np.float64
MIN_ANGLE_DELTA = np.finfo(DTYPE).eps * 1e6
LINE_EXTENSION_LENGTH = np.array(WIDTH * 3 / 4, dtype=DTYPE)

CENTER = np.array([WIDTH / 2, HEIGHT / 2], dtype=DTYPE)
RADIUS = np.array(HEIGHT / 3, dtype=DTYPE)
TAU = np.array(np.pi * 2, dtype=DTYPE)

LINE_WIDTH = 3

FPS = 60

NUM_STARTING_POINTS = 512
MULTIPLES_PER_STARTING_POINT = 30
# MULTIPLES_PER_STARTING_POINT = 30 * 2
# MULTIPLES_PER_STARTING_POINT = 30 * 5 * 2
# MULTIPLES_PER_STARTING_POINT = 30 * 30
# MULTIPLES_PER_STARTING_POINT = 1

RESUME = True


def write_frame(frame_data):
    frame_num, colors, start_points, end_points = frame_data

    frame_path = os.path.join(FRAMES_DIR, f'frame_{frame_num}.png')
    if os.path.exists(frame_path):
        return

    # Initialize our surface and context.
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    cr = cairo.Context(surface)

    # Paint the frame black.
    cr.set_source_rgb(0, 0, 0)
    cr.set_operator(cairo.Operator.SOURCE)
    cr.paint()
    cr.set_operator(cairo.Operator.SCREEN)

    # Set the line width.
    cr.set_line_width(LINE_WIDTH)

    # Draw each line.
    for i in range(len(colors)):
        cr.set_source_rgb(*colors[i])
        cr.move_to(*start_points[i])
        cr.line_to(*end_points[i])
        cr.stroke()

    # Write the frame to disk.
    surface.write_to_png(frame_path)


def main():
    # Delete the frames directory if it exists then recreate an empty
    # frames directory.
    if os.path.exists(FRAMES_DIR) and not RESUME:
        shutil.rmtree(FRAMES_DIR)
    if not os.path.exists(FRAMES_DIR):
        os.mkdir(FRAMES_DIR)

    # Get the angles for each of our starting points.
    start_angles = np.arange(NUM_STARTING_POINTS, dtype=DTYPE) / NUM_STARTING_POINTS * TAU

    # Get a color for each starting angle. Angle 0 will be fully
    # saturated red, and then it will cycle through all the fully
    # saturated colors (orange, yellow, green, ...) as the angle
    # increases clockwise, with angle tau coming back to fully saturated
    # red again.
    colors = np.clip(
        np.stack(
            [
                (-np.abs((-start_angles + TAU / 2) % TAU - TAU / 2) + TAU / 3) * 6 / TAU,
                (-np.abs((-start_angles - TAU / 6) % TAU - TAU / 2) + TAU / 3) * 6 / TAU,
                (-np.abs((-start_angles + TAU / 6) % TAU - TAU / 2) + TAU / 3) * 6 / TAU,
            ],
            axis=1,
        ),
        0,
        1,
    )

    # Get the multiples for each frame.
    multiples = np.linspace(
        1, NUM_STARTING_POINTS, ((NUM_STARTING_POINTS - 1) * MULTIPLES_PER_STARTING_POINT) + 1
    )
    # multiples = np.linspace(
    #     1, NUM_STARTING_POINTS + 1, NUM_STARTING_POINTS * MULTIPLES_PER_STARTING_POINT + 1,
    # )

    # If I only want to render a section of the sequence, I reduce the
    # `multiples` array here to the section that should be rendered.
    # multiples = multiples[-MULTIPLES_PER_STARTING_POINT:]
    # multiples = multiples[-MULTIPLES_PER_STARTING_POINT * 2 :]
    # multiples = multiples[: MULTIPLES_PER_STARTING_POINT * 32]

    # Expand the first dimension of `multiples` and the last dimension
    # of `starting_angles` so that they can be broadcast together when
    # multiplied.
    multiples = multiples[None, ...]
    start_angles = start_angles[..., None]

    # Calculate the difference in angle between the starting point and
    # the ending point, and make sure they are at least
    # `MIN_ANGLE_DELTA` apart (this makes it so that if the points would
    # have landed at the same point, they will instead be just slightly
    # apart so that a line will be drawn tangent to the circle).
    delta_angles = (multiples * start_angles - start_angles) % TAU
    delta_angles = np.clip(delta_angles, MIN_ANGLE_DELTA, TAU - MIN_ANGLE_DELTA)

    # Get the starting angles and ending angles. These are rotated so
    # that they are displayed in desired rotation.
    start_angles -= TAU / 4
    end_angles = start_angles + delta_angles

    # Calculate the starting and ending points on the circle form the
    # starting and ending angles.
    start_points = CENTER + RADIUS * np.stack([np.cos(start_angles), np.sin(start_angles)], axis=2)
    end_points = CENTER + RADIUS * np.stack([np.cos(end_angles), np.sin(end_angles)], axis=2)

    # Extend the line that connects the points so that it goes off the
    # edge of the screen.
    diffs = end_points - start_points
    unit_diffs = diffs / np.linalg.norm(diffs, axis=2, keepdims=True)
    start_points = start_points - unit_diffs * LINE_EXTENSION_LENGTH
    end_points = end_points + unit_diffs * LINE_EXTENSION_LENGTH

    # Get the number of frames and generate a list of frame data tuples,
    # where each tuple contains all the data needed to generate that
    # frame.
    num_frames = start_points.shape[1]
    frame_data_list = [
        (frame_num, colors, start_points[:, frame_num], end_points[:, frame_num])
        for frame_num in range(num_frames)
    ]

    print(f'frames: {len(frame_data_list)}, mins: {len(frame_data_list) / FPS / 60}')

    # We create a pool of processes and for each tuple of frame data in
    # our frame data list, we pass that tuple of frame data to a process
    # and that process calls `write_frame()` passing it the tuple of
    # frame data as the argument. Then the `write_frame()` function
    # draws the frame and writes it to disk.
    with mp.Pool(mp.cpu_count()) as p:
        for _ in tqdm.tqdm(p.imap_unordered(write_frame, frame_data_list), total=num_frames):
            # This loop is just a simple way to wrap our pool iterator
            # with tqdm so that we can track the progress of our script,
            # and since we don't do anything with the data returned from
            # the `write_frame()` calls so we just write `pass` here.
            pass


if __name__ == '__main__':
    main()
