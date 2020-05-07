import xml.etree.ElementTree as ET
import pickle
import os,sys
from os import listdir, getcwd
from os.path import join

sets = [('2012', 'train'), ('2012', 'val'),
        ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["person"]


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x, y, w, h)


def convert_annotation(year, image_id):
    in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml' % (year, image_id))
    out_file = open('VOCdevkit/VOC%s/labels/%s.txt' % (year, image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(
            xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " +
                       " ".join([str(a) for a in bb]) + '\n')


wd = getcwd()

for year, image_set in sets:
    VOC = 'VOCdevkit/VOC%s' % (year)
    labels = '%s/labels' % (VOC)
    ImageSets_Main = '%s/ImageSets/Main/%s.txt' % (VOC, image_set)
    JPEGImages = '%s/JPEGImages' % (VOC)

    if not os.path.exists(labels):
        os.makedirs(labels)

    image_ids = open(ImageSets_Main).read().strip().split()
    list_file = open('%s_%s.txt' % (year, image_set), 'w')

    for image_id in image_ids:
        JPEG_file = '%s/%s.jpg' % (JPEGImages, image_id)
        if os.path.exists(JPEG_file):
            list_file.write('%s\n' % (JPEG_file))
            convert_annotation(year, image_id)

    list_file.close()

os.system("cat 2007_train.txt 2007_val.txt 2007_test.txt 2012_train.txt 2012_val.txt > total.txt")
