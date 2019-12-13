import argparse
import os
import datetime
import json
import numpy as np
import sys
import cv2
import time

from tqdm import tqdm

dir_name = os.path.dirname(__file__)
sys.path.append(os.path.join(dir_name, '../'))
sys.path.append(os.path.join(dir_name, '../PoseEstimation/')) 
sys.path.append(os.path.join(dir_name, '../utils'))

from data_preparation.prepare_source import prepare_source
from data_postprocessing.normalization import normalize
from data_postprocessing.transfer import test_transfer
from data_postprocessing.make_gif import make_gif


def record_and_makegif(target_dir, run_name):

    countdown(t=5)

    source_dir = os.path.join(dir_name, '../../data/sources', run_name)
    os.makedirs(source_dir, exist_ok=True)

    video = record_video(source_dir)

    prepare_source(source_dir, frames=True)

    normalize(source_dir, target_dir)

    test_transfer(source_dir, 'example_target')

    make_gif(source_dir, os.path.join(dir_name, '../../results', 'example_target'))


def record_video(source_dir):
    img_dir = os.path.join(source_dir, 'images')
    os.makedirs(img_dir, exist_ok=True)

    stream = cv2.VideoCapture('http://127.0.0.1:8080')

    # Check if the webcam is opened correctly
    if not stream.isOpened():
        raise IOError("Cannot open webcam")

    for i in tqdm(range(100), 'acquiring frames'):
        ret, frame = stream.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(img_dir, '{:05d}.png'.format(i)), frame)

    stream.release()


def countdown(t):
    while t > 0:
        print(t)
        t -= 1
        if t == 0:
            print('DANCING TIME!')
            break
        time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Record short video and make a gif of transferred target')
    parser.add_argument('-t', '--target-dir', type=str,
                        default=os.path.join(dir_name, '../../data/targets/example_target'),
                        help='Path to the folder where the target video is saved. One video per folder!')
    parser.add_argument('-r', '--run-name', type=str,
                        default=datetime.datetime.now().strftime("%Y-%b-%d-%H-%M-%S"),
                        help='Name of the current run')
    args = parser.parse_args()
    record_and_makegif(args.target_dir, args.run_name)