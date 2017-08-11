import argparse
import lib.viewer
import lib.saver

def main(args):
    with open(args.labels_file) as f:
        # read the labels file, each line is a label name
        labels=f.read().split('\n')
    print("%d labels was created"%len(labels))
    if len(labels)==0:
        print("no labels found")
        return
    saver=lib.saver.BoxSaver(args.save_dir,args.write_im)
    lib.viewer.GUILabeler(labels,args.video_file,saver,args.border)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('video_file',help='video file path to label',type=str)
    parser.add_argument('labels_file',help='labels file path(split by \\n)',type=str)
    parser.add_argument('save_dir',help='label result save path',type=str)
    parser.add_argument('--write_im',help='write every cropped image to each label directory',action='store_true')
    parser.add_argument('--border',help='the border of the center clip filed (white line around the video)',type=int,default=10)
    args=parser.parse_args()
    main(args)