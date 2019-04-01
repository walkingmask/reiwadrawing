import argparse
import json

import cv2


class PointsRecorder:
    def __init__(self):
        self.points = {}
        self.buffer = []
        self.index = 0
        self.buffer_count = 0

    def rec(self, x, y):
        self.buffer.append([x, y])
        self.buffer_count += 1
        if self.buffer_count == 4:
            print(self.index, ':', self.buffer)
            self.points[self.index] = self.buffer
            self.index += 1
            self.buffer_count = 0
            self.buffer = []

    def skip(self):
        self.points[self.index] = None
        self.index += 1
        self.buffer_count = 0
        self.buffer = []


def mouse_event(event, x, y, flags, recorder):
    if event == cv2.EVENT_LBUTTONUP:
        recorder.rec(x, y)


def get(mov_path):
    mov = cv2.VideoCapture(mov_path)

    recorder = PointsRecorder()

    cv2.namedWindow('mov', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('mov', mouse_event, recorder)

    while True:
        ret, frame = mov.read()
        if not ret:
            break
        cv2.imshow('mov', frame)
        k = cv2.waitKey() & 0xFF
        if k == ord('q'):
            break
        elif k == ord('s'):
            recorder.skip()

    cv2.destroyAllWindows()
    mov.release()

    return recorder


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mov_path')
    parser.add_argument('out_path')
    args = parser.parse_args()

    rec = get(args.mov_path)

    with open(args.out_path, 'w') as f:
        json.dump(rec.points, f)
