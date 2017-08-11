import os
import cv2
import numpy as np

from lib.tracker import Tracker


class LabelStat():
    def __init__(self,labels_name,label_height=50,label_width=300):
        self.labels_name = labels_name
        self.label_im = np.ones([label_height * len(labels_name), label_width, 3], np.uint8) * 100
        self.label=0
        self.h=label_height
        self.w=label_width
        self.box_color=(0,0,80)
        self.draw_labels()
        self.select(0)

    def select(self,y):
        idx=y/self.h
        cv2.rectangle(self.label_im, (0, self.label * self.h), (self.w, (self.label + 1) * self.h),
                      (100, 100, 100), 3)
        self.label = idx
        cv2.rectangle(self.label_im, (0, idx * self.h), (self.w - 1, (idx + 1) * self.h), self.box_color, 3)
        cv2.imshow("label", self.label_im)

    def draw_labels(self):
        for idx, label in enumerate(self.labels_name):
            cv2.rectangle(self.label_im, (0, idx * self.h), (self.w, (idx + 1) * self.h), (255, 255, 255))
            cv2.putText(self.label_im, label, (0, int((idx + 0.5) * self.h)), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255))
        cv2.imshow("label", self.label_im)

    def get_label_name(self):
        return self.labels_name[self.label]

class VideoStat():
    def __init__(self,border=30):
        self.is_drug=False
        self.boxes=[]
        self.trackers=[]
        self.colors=[]
        self.labels=[]
        self.p0=(0,0)
        self.p1=(0,0)
        self.p=(0,0) # the mouse pointer's current position
        self.video_im=np.ones([320,320,3],np.uint8)
        self.border=border
        self.frame_id=0

    def update_im(self,im):
        self.video_im = im.copy()
        cv2.rectangle(self.video_im,
                      (self.border,self.border),(self.video_im.shape[1]-self.border,self.video_im.shape[0]-self.border),
                      (255,255,255))
        for i,box in enumerate(self.boxes):
            cv2.rectangle(self.video_im,box[0],box[1],self.colors[i])
            cv2.putText(self.video_im,self.labels[i],box[0],cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        cv2.imshow("video", self.video_im)

    def update_box(self):
        border=self.border
        remove_list=[]
        for i,tracker in enumerate(self.trackers):
            p0,p1=tracker.track(self.video_im)
            if              self.video_im.shape[0] - border > p0[1] > 0 + border and \
                            self.video_im.shape[0] - border > p1[1] > 0 + border and \
                            self.video_im.shape[1] - border > p0[0] > 0 + border and \
                            self.video_im.shape[1] - border > p1[0] > 0 + border:
                self.boxes[i]=[p0,p1]
            else:
                remove_list.append(i)
        map(self.box_remove,remove_list)


    def update(self,im):
        self.frame_id+=1
        self.update_box()
        self.update_im(im)


    def draw_update(self,im,label_name=''):
        self.video_im=im.copy()
        cv2.rectangle(self.video_im,self.p0,self.p,(255,255,255))
        cv2.putText(self.video_im, label_name, self.p0, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow("video", self.video_im)

    def box_remove(self,idx):
        print "remove box", self.boxes[idx]
        del self.boxes[idx]
        del self.colors[idx]
        del self.trackers[idx]
        del self.labels[idx]

    def box_append(self,label_name):
        if self.p0[0]-self.p1[0]>=0 or self.p0[1]-self.p1[1]>=0:
            return
        self.boxes.append([self.p0,self.p1])
        self.colors.append([255,0,255])
        tracker=Tracker()
        tracker.start(self.video_im,self.p0,self.p1)
        self.trackers.append(tracker)
        self.labels.append(label_name)

    def get_boxes(self):
        return zip(self.boxes,self.labels)

cv2.namedWindow("video")
cv2.namedWindow("label")
# cv2.namedWindow("show")

class GUILabeler():
    def __init__(self,labels,video_file,box_saver,border=30):
        """
        the GUI Labeler
        :param labels: the labels name string list
        :param video_file: the video file path
        :param border: the border of the center clip filed (white line around the video)
        :param save_dir: label result save path
        :param save_im: if write every cropped image to each label directory
        """
        self.cam = cv2.VideoCapture(video_file)
        self.video_stat = VideoStat(border)
        self.label_stat = LabelStat(labels)
        self.labels=labels
        self.box_saver=box_saver
        cv2.setMouseCallback("video", self.video_click)
        cv2.setMouseCallback("label", self.label_click)
        self.run()

    def run(self):
        stop = False
        _, im = self.cam.read()
        while 1:
            if not self.video_stat.is_drug and not stop:
                _, im = self.cam.read()
                self.video_stat.update(im)
                self.box_saver.save(im,self.video_stat.frame_id,self.video_stat.get_boxes())
            else:
                if self.video_stat.is_drug:
                    self.video_stat.draw_update(im, self.label_stat.get_label_name())
            chr=cv2.waitKey(1) & 0xFF
            if chr==ord(' '): # press space to stop the frame
                stop= not stop
            if chr==27: # Esc key to exit
                break


    def video_click(self,e, x, y, flags, param):
        if e == cv2.EVENT_LBUTTONDOWN:
            self.video_stat.is_drug = 1
            self.video_stat.p0 = (x, y)
            print("rect start", x, y)
        elif e == cv2.EVENT_LBUTTONUP:
            self.video_stat.is_drug = 0
            self.video_stat.p1 = (x, y)
            print("rect end", x, y)
            self.video_stat.box_append(self.label_stat.get_label_name())

        self.video_stat.p=(x,y)

    def label_click(self,e, x, y, flags, param):
        if e == cv2.EVENT_LBUTTONDOWN:
            self.label_stat.select(y)



