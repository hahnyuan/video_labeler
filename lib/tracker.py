import dlib
import cv2


class Tracker():
    def __init__(self):
        self.t=dlib.correlation_tracker()

    def start(self,im,p0,p1):
        # p0 is leftupper position of the obj, p1 is rightbottom of the obj
        self.t.start_track(im, dlib.rectangle(p0[0],p0[1], p1[0], p1[1]))

    def track(self,im):
        self.t.update(im)
        # print self.t.get_position()
        position=self.t.get_position()
        return (int(position.left()),int(position.top())),(int(position.right()),int(position.bottom()))