import sys
import os
import cv2
from PIL import Image

def mosaic(src, ratio):
    small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
    # slice(start:stop[:step])
    #     src.shape          : (height, width, depth)
    #     src.shape[:2]      : (height, width)
    #     src.shape[:2][::-1]: (width, height)
    return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

args = sys.argv

if len(args) != 3:
    sys.exit("Usage: python %s FILEPATH DURATION" % args[0])

filepath = args[1]
duration = int(args[2])
if duration <= 0:
    sys.exit("Error: DURATION <= 0")

# OpenCV: BGR
# Pillow: RGB
# BGR --> RGB
src = cv2.cvtColor(cv2.imread(filepath), cv2.COLOR_BGR2RGB)

imgs = [Image.fromarray(mosaic(src, 1.0 / i)) for i in range(1, 25)[::-1]]

outpath = os.path.dirname(os.path.abspath(__file__)) + '/out/'
if not os.path.isdir(outpath):
    os.mkdir(outpath)
imgs[0].save(outpath + os.path.splitext(os.path.basename(filepath))[0] + '.gif',
             save_all=True, append_images=imgs[1:], optimize=False, duration=duration)
