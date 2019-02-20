#! /usr/bin/python
# -*- coding: utf-8 -*-
"""VGG-16 for ImageNet using TL models."""

# import sys
# sys.path.append("D:\\tensorlayer2")
# import ipdb

import time
import numpy as np
import tensorflow as tf
import tensorlayer as tl
from tensorlayer.models.imagenet_classes import class_names

tf.logging.set_verbosity(tf.logging.DEBUG)
tl.logging.set_verbosity(tl.logging.DEBUG)


# get the whole model
vgg = tl.models.VGG16()

# restore pre-trained VGG parameters
sess = tf.InteractiveSession()

vgg.restore_weights(sess)

img1 = tl.vis.read_image('data/tiger.jpeg')
img1 = tl.prepro.imresize(img1, (224, 224))
img1 = img1.astype(np.float32)
# rescale pixels values in the range of 0-1
img1 = img1 / 255.0
if ((0 <= img1).all() and (img1 <= 1.0).all()) is False:
    raise Exception("image value should be [0, 1]")

start_time = time.time()
vgg.eval()
output = vgg(img1)
probs = tf.nn.softmax(output.outputs).eval()[0]
print("  End time : %.5ss" % (time.time() - start_time))
preds = (np.argsort(probs)[::-1])[0:5]
for p in preds:
    print(class_names[p], probs[p])
