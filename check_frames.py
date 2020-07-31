import os
import imghdr

CUR_DIR = os.path.join(os.path.dirname(__file__))
FRAMES_DIR = os.path.join(CUR_DIR, 'frames_512_30_3')


def main():
    num_frames = len(
        [path for path in os.listdir(FRAMES_DIR) if os.path.isfile(os.path.join(FRAMES_DIR, path))]
    )
    has_missing_or_corrupt_frame = False
    for frame_num in range(num_frames):
        frame_path = os.path.join(FRAMES_DIR, f'frame_{frame_num}.png')
        if not os.path.exists(frame_path):
            print('Missing frame: {frame_num}')
            has_missing_or_corrupt_frame = True
        elif imghdr.what(frame_path) != 'png':
            print('Corrupt frame: {frame_num}')
            has_missing_or_corrupt_frame = True

    if not has_missing_or_corrupt_frame:
        print(f'All {num_frames} were found.')


if __name__ == '__main__':
    main()
