# Data Labeler for Video

 Providing a tool for conveniently label the objects in video, using the powerful object tracking.

 The video_labeler is released under the MIT License (refer to the LICENSE file for details).

### features

1. There is a GUI make what you see is what you get.
2. The powerful object tracking method can track the objects automatically, which can avoid label a object repeatedly.
3. The output can be converted to many format (such as VOC like) using the scripts video_labeler provided.(developing)

![demo1.jpg](https://raw.githubusercontent.com/hahnyuan/video_labeler/master/example/demo1.jpg)

### requirements

- Python 2.7
- Linux or Mac OS, I'm going to develop the Windows version.
- Opencv-python, you can install it using pip
- Dlib, you can install it using pip

# Track labeler

`track_labeler.py` uses the powerful object tracking method, which can avoid label a object repeatedly.

Command: `python track_labeler.py [-h] [--write_im] [--border BORDER] video_file labels_file save_dir`
- video_file is the video file path to label
- labels_file is the labels file path(split by \n)
- save_dir is the label result save path
- --write_im open the function write every cropped image to each label director
- --border BORDER sets the border of the center clip filed (white line around the video in GUI)

For example `python track_labeler.py data/1.MOV data/labels_name.txt output`

The `labels_file` should contain the name the classes name, split by line break (\n).
So you can select them in the `label` GUI windows.

### Manipulation

- Select a label from the `label` GUI windows.
- Hold the left bottom of your mouse and drug a rectangle.
- Press `Space` will stop the video play, so you can clearly view your label.
- Press `Esc` will exit the labeler.

### Output

The labeler will write the file `labels.txt` in your `save_dir`. The output format as "frame_id label x0 y0 x1 y1":
- frame_id: the number of frame in the video.
- label: the object label name.
- x0, y0: the left upper position of the object rectangle.
- x1, y1: the left upper position of the object rectangle.

Notice: If there exists a file named `labels.txt`, the new information will append in it.

If the `--write_im` was selected, the objects will be saved in each label director.
The file format as "savedir/labelname/frame_idx.jpg"
- frame: the number of frame in the video.
- idx: the idx the object at that frame.

# Simple labeler

doc coming soon