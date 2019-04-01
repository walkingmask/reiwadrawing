import argparse

import cv2


def trim(mov_path, out_path, zoom=0.5):
    mov = cv2.VideoCapture(mov_path)

    width = int(float(mov.get(cv2.CAP_PROP_FRAME_WIDTH)) * zoom)
    height = int(float(mov.get(cv2.CAP_PROP_FRAME_HEIGHT)) * zoom)
    fps = mov.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    cv2.namedWindow("mov", cv2.WINDOW_NORMAL)
    start = False

    while True:
        ret, frame = mov.read()
        if not ret:
            break

        if not start:
            cv2.imshow('mov', frame)
            k = cv2.waitKey(0) & 0xFF
            if k == ord('q'):
                break
            if k == ord('s'):
                start = True

        if start:
            frame = cv2.resize(frame, dsize=(width, height))
            out.write(frame)

    out.release()
    mov.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mov_path')
    parser.add_argument('out_path')
    parser.add_argument('-z', '--zoom', type=float, default=0.5)
    args = parser.parse_args()

    trim(args.mov_path, args.out_path, args.zoom)
