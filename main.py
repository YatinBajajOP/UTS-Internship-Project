import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow.keras
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
# from keras.models import *
# from keras.layers import *

from types import MethodType
import json
from tqdm import tqdm
import numpy as np
import itertools
from tensorflow.keras.utils import get_file

from tensorflow.keras.utils import Sequence
from tensorflow.keras.utils import SequenceEnqueuer
from tensorflow.keras.utils import OrderedEnqueuer
from tensorflow.keras.utils import GeneratorEnqueuer

from tensorflow import keras
model = keras.models.load_model('Image_Class1.h5')

from Pratapgarh.predict import predict
model.predict_segmentation = MethodType(predict, model)

IMAGE_ORDERING_CHANNELS_FIRST = "channels_first"
IMAGE_ORDERING_CHANNELS_LAST = "channels_last"
# Default IMAGE_ORDERING = channels_last
IMAGE_ORDERING = IMAGE_ORDERING_CHANNELS_LAST

if IMAGE_ORDERING == 'channels_first':
    MERGE_AXIS = 1
elif IMAGE_ORDERING == 'channels_last':
    MERGE_AXIS = -1

from PIL import Image
import matplotlib.pyplot as plt


# start = time.time()

# input_image = 'UP_PRATAPGARH/SPLITTED_IMAGE/307100_Pratapgarh_09_01.png'
# input_image = 'UP_PRATAPGARH/SPLITTED_IMAGE/307100_Pratapgarh_07_02.png'
#input_image = 'Pratapgarh/IMAGE/307095_Pratapgarh_01_04.png'

from weather_report import *

loc = input("Enter Location Name : ")

input_image = input("Enter Loaction Image file : ")

weather(loc)

out = model.predict_segmentation(
    inp=input_image,
    out_fname="out.png"
)

# from bounding_box import *
#
# bounding_box(input_image)

import cv2
import numpy as np

# Reading Input Image
img1 = cv2.imread(input_image)

# Reading output Image
img2 = cv2.imread('out.png')

# concatanate image Horizontally
output = np.concatenate((img1, img2), axis=1)

cv2.imshow('Output Image', output)

cv2.waitKey(0)
cv2.destroyAllWindows()

# fig, axs = plt.subplots(1, 2, figsize=(20, 20), constrained_layout=True)

# img_orig = Image.open(input_image)
# axs[0].imshow(img_orig)
# axs[0].set_title('original image-002.jpg')
# axs[0].grid(False)
#
# axs[1].imshow(out)
# axs[1].set_title('prediction image-out_model1.png')
# axs[1].grid(False)

# validation_image = "/kaggle/input/semantic-drone-dataset/semantic_drone_dataset/label_images_semantic/002.png"
# axs[2].imshow( Image.open(validation_image))
# axs[2].set_title('true label image-002.png')
# axs[2].grid(False)


# done = time.time()
# elapsed = done - start