#! /usr/bin/env python

import cv2
import sys


vc = cv2.VideoCapture(0)

vc.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1280)
vc.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,720)

if not vc.isOpened():
    print("Could not open!");
    sys.exit(1)

for count in range(0,5):
    success,frame = vc.read()
    if not success:
        print("Could not read!");
        sys.exit(1)
    cv2.imwrite('capture_%02d.png' % count,frame)



vc.release()
vc = None
