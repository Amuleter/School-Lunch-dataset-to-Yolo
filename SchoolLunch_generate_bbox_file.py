
import os
from PIL import Image

# modify the directories and class file to fit
datapath = '/school_lunch/Images'
labelpath = '/school_lunch/Annotations'
covertpath = '/school_lunch/Convert'

def convert_yolo_bbox(img_size, box):
    # img_bbox file is [0:img] [1:left X] [2:bottom Y] [3:right X] [4:top Y]
    dw = 1./img_size[0]
    dh = 1./img_size[1]
    x = (int(box[1]) + int(box[3]))/2.0
    y = (int(box[2]) + int(box[4]))/2.0
    w = abs(int(box[3]) - int(box[1]))
    h = abs(int(box[4]) - int(box[2]))
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    # Yolo bbox is center x, y and width, height
    return (x,y,w,h)


def get_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


def generate_bbox_file(datapath, labelpath, filename):
    dataDir = os.path.join(datapath)
    labelDir = os.path.join(labelpath)
    convertDir = os.path.join(covertpath)
    bb_filename = os.path.join(labelpath, filename+'.txt')
    if not os.path.exists(convertDir):
        os.makedirs(convertDir)
    with open(bb_filename, 'r') as fp:
      lines = fp.readlines()

    yolo_bboxes = []
    for line in lines:
      # img_bbox file is [0:img] [1:left X] [2:bottom Y] [3:right X] [4:top Y]
      img_bbox = line.strip('\n').split(' ')
      if img_bbox[0] != 'img':
        img_bbox_filename = os.path.join(dataDir, filename+'.txt')
        #with open(img_bbox_filename, 'w') as f:
        # [number of bbox]
        # [left X] [top Y] [right X] [bottom Y] [class name]
        #f.write('1\n')
        #f.write('%s %s %s %s %s\n' %(img_bbox[0], img_bbox[1], img_bbox[4], img_bbox[3], img_bbox[2]))
        image_filename = os.path.join(dataDir, filename+'.jpg')
        yolo_label_filename = os.path.join(labelDir, filename+'.txt')
        yolo_bbox = convert_yolo_bbox(Image.open(image_filename).size, img_bbox)
        yolo_bboxes.append(img_bbox[0] + ' ' + ' '.join(map(str, yolo_bbox)) + '\n')

        # Write the YOLO bboxes to a file in the new folder.
    new_bb_filename = os.path.join(convertDir, filename + '.txt')
    with open(new_bb_filename, 'w') as f:
      for yolo_bbox in yolo_bboxes:
        f.write(yolo_bbox)



for file in get_files(datapath):
    imgname = os.path.splitext(file)[0]
    generate_bbox_file(datapath, labelpath, imgname)
    print("generated %s" %(imgname))

