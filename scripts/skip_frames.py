import argparse

import cv2


def skip(mov_path, out_path, skip=5):
    mov = cv2.VideoCapture(mov_path)

    width = int(mov.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(mov.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = mov.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, int(fps / skip), (width, height))

    frames = 0

    for i in range(10000):
        ret, frame = mov.read()
        if not ret:
            break

        if i % skip == 0:
            out.write(frame)
            frames += 1

    out.release()
    mov.release()
    print(frames)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mov_path')
    parser.add_argument('out_path')
    parser.add_argument('-s', '--skip', type=int, default=5)
    args = parser.parse_args()

    skip(args.mov_path, args.out_path, args.skip)
