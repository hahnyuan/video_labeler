import os
import cv2

class BoxSaver():
    def __init__(self,save_dir,save_im=False):
        self.save_dir=save_dir
        self.save_im=save_im
        self.label_file='%s/labels.txt'%(self.save_dir)

    def save(self,im,frame_id,boxes_iter):
        for idx,(box,label) in enumerate(boxes_iter):
            p0, p1 = box
            with open(self.label_file,'a') as f:
                # write format frame_id label x0 y0 x1 y1
                f.write("%d %s %d %d %d %d\n"%(frame_id,label,p0[0],p1[0],p0[1],p1[1]))
            if self.save_im:
                filename = '%s/%s/%d_%d.jpg' % (self.save_dir,label, frame_id, idx)
                dir=os.path.split(filename)[0]
                if not os.path.exists(dir):
                    os.makedirs(dir)
                filename=os.path.abspath(filename)
                obj_im=im[p0[1]:p1[1],p0[0]:p1[0]]
                cv2.imwrite(filename,obj_im)