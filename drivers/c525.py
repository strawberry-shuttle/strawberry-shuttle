__author__ = 'Vijay Ganesan'

import cv2
from misc.log import Log

class Camera_C525():
    """Logitech C525 Camera Class"""
    def __init__(self,num=0,x=1280,y=720):
        self.id = num
        self.vc = cv2.VideoCapture(num)
        self.vc.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,x)
        self.vc.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,y)

        if not self.vc.isOpened():
            l = Log()
            l.ShowDebug("Camera_C525: Could not open camera %d, res %d x %d" % (num,x,y))
        return

    def __del__(self):
        self.vc.release()
        del self.vc
        del self.id

    def takePicture(self,max_count=5):
        for count in range(0,max_count):
            success,frame = self.vc.read()
            if not success:
                l = Log()
                l.ShowDebug("Camera_C525: Could not read %d, max count %d" % (self.id,max_count))
            cv2.imwrite('capture_%02d.png' % count,frame)