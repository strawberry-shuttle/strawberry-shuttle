__author__ = 'Vijay Ganesan'

import cv2
from misc.log import Log

class Camera_C525():
    """
    Logitech C525 Camera Class
    
    Driver class to handle camera related operations. Each class instance can handle a different camera.
    """
    def __init__(self,num=0,x=1280,y=720):
        """
        
        Input: int(num = cameraID),int(x = x resolution), int(y = y resolution)
        Output: N/A
        
        Constructor for C525 driver class. Takes the camera ID (check /dev/ for the ID), and the x and y resolutions.
        """
        self.id = num
        self.vc = cv2.VideoCapture(num)
        self.vc.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,x)
        self.vc.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,y)

        if not self.vc.isOpened():
            l = Log()
            l.ShowDebug("Camera_C525: Could not open camera %d, res %d x %d" % (num,x,y))
        return

    def __del__(self):
        """
        
        Input: N/A
        Output: N/A
        
        Destructor for the camera class. Necessary to handle camera cleanup code. Should never be explicitly called.
        """
        self.vc.release()
        del self.vc
        del self.id

    def takePicture(self,max_count=5):
        """
        
        Input: int(max_count = number of pictures to take)
        Output: N/A
        
        Send command to camera to take photos. The camera takes a little bit to warm up, so taking several pictures might be necessary for quality.
        """    
        for count in range(0,max_count):
            success,frame = self.vc.read()
            if not success:
                l = Log()
                l.ShowDebug("Camera_C525: Could not read %d, max count %d" % (self.id,max_count))
            cv2.imwrite('capture_%02d.png' % count,frame)