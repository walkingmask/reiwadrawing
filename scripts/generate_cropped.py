import argparse
import json
from pathlib import Path

import cv2
import numpy as np


def load_points(points_path):
    with open(points_path) as f:
        points_dict = json.load(f)
    points_list = []
    for i in range(len(points_dict)):
        points_list.append(points_dict[str(i)])
    return points_list


def crop(mov, points, out_path):
    for i in range(10000):
        ret, frame = mov.read()
        if not ret:
            break
        if points[i]:
            _points = np.array(points[i])
            alpha = np.ones(frame.shape[:2] + (1,), dtype=np.uint8) * 255
            cv2.fillConvexPoly(frame, points=_points, color=(0, 0, 0), lineType=cv2.LINE_AA)
            cv2.fillConvexPoly(alpha, points=_points, color=(0), lineType=cv2.LINE_AA)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.dstack((frame, alpha))
        cv2.imwrite("{}/i{:03d}.png".format(out_path, i), frame)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mov_path')
    parser.add_argument('points_path')
    parser.add_argument('out_dir_path')
    args = parser.parse_args()

    mov = cv2.VideoCapture(args.mov_path)
    out_dir = Path(args.out_dir_path).absolute()
    if not out_dir.exists():
        print("{} not found".format(out_dir))
        exit(1)
    points = load_points(args.points_path)

    crop(mov, points, out_dir)

    mov.release()
