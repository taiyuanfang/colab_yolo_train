import xml.etree.ElementTree as ET
import pickle
import os, sys, shutil
from os import listdir, getcwd
from os.path import join

def copy_file(src_folder, dst_folder, image_id, sub_folder, file_ext):
    src = '%s/%s/%s.%s' % (src_folder, sub_folder, image_id, file_ext)
    if not os.path.exists(src):
        return
    dst = '%s/%s/%s.%s' % (dst_folder, sub_folder, image_id, file_ext)
    shutil.copy(src, dst)

def process_line(dst_folder, line, list_file):
    nodes = line.strip().split('/')
    if len(nodes) != 4:
        return
    src_folder = '%s/%s' % (nodes[0], nodes[1])
    image_id = nodes[3].split('.')[0]
    copy_file(src_folder, dst_folder, image_id, 'Annotations', 'xml')
    copy_file(src_folder, dst_folder, image_id, 'JPEGImages', 'jpg')
    copy_file(src_folder, dst_folder, image_id, 'labels', 'txt')
    copy_file(src_folder, dst_folder, image_id, 'SegmentationClass', 'png')
    copy_file(src_folder, dst_folder, image_id, 'SegmentationObject', 'png')
    list_file.write('%s/JPEGImages/%s.jpg\n' % (dst_folder, image_id))


seq_begin = 0
seq_end = 0
train_count = 0

if len(sys.argv) > 1:
    seq_begin = int(sys.argv[1])

if len(sys.argv) > 2:
    seq_end = int(sys.argv[2])
else:
    seq_end = (seq_begin + 1000)

train_count = int(0.8 * (seq_end - seq_begin))

VOC = 'VOC_%d_%d' % (seq_begin, seq_end)
if not os.path.exists(VOC):
    os.makedirs(VOC)
    os.makedirs('%s/Annotations' % (VOC))
    os.makedirs('%s/JPEGImages' % (VOC))
    os.makedirs('%s/labels' % (VOC))
    os.makedirs('%s/SegmentationClass' % (VOC))
    os.makedirs('%s/SegmentationObject' % (VOC))

train_txt = open('%s/train.txt' % (VOC), 'w')
test_txt = open('%s/test.txt' % (VOC), 'w')
seq = 0

with open('total.txt','r') as fp:
    while seq < seq_end:
        line = fp.readline().strip()
        if not line:
            break
        seq += 1
        if seq < seq_begin:
            continue
        print(seq, line)
        if train_count > 0:
            process_line(VOC, line, train_txt)
            train_count -= 1
        else:
            process_line(VOC, line, test_txt)

