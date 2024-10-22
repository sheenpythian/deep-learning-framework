from config import Config

import datetime, logging, os, sys


'''
Set up the Python Logger using class Config().
'''
logname = "mnist_example.log"
logger = logging.getLogger(logname)

conf = Config()
conf.configure(config=None)

formatter = logging.Formatter(conf.configuration["logging"]["formatter"])

if conf.configuration["logging"]["handler"] == "stream":
    handler = logging.StreamHandler()
    handler.setStream(getattr(sys, conf.configuration["logging"]["stream"]))

if conf.configuration["logging"]["handler"] == "file":
    logdate = datetime.datetime.now()
    handler = logging.FileHandler(f'{os.environ["PWD"]}/log/{logdate.strftime("%Y%m%d")}_{logname}')

handler.setFormatter(formatter)
logger.addHandler(handler)

if hasattr(logging, conf.configuration["logging"]["level"].upper()):
    logger.setLevel(getattr(logging, conf.configuration["logging"]["level"].upper()))
    logger.warning(f'Package loglevel has been set to {logger.getEffectiveLevel()}')

'''
Configure argument parsing, for convenience.
'''
import argparse

parser = argparse.ArgumentParser()

''' Optional backend override.'''
parser.add_argument('--keras-backend-override', action='store', dest='keras_backend_override')

args = parser.parse_args()

'''
Configure and import deep learning modules.
'''
os.environ["KERAS_BACKEND"] = args.keras_backend_override or conf.configuration["keras"]["backend"]
logger.info(f'Configuring Keras backend as "{os.environ["KERAS_BACKEND"]}".')

import keras, numpy, tensorflow


'''
The keras mnist dataset is a set of character images. Each image is 28 x 28 BW pixels.
'''

'''
Load some data from the keras mnist dataset into dataframes, split for training and testing.
x_* hold images, and y_* hold labels.
'''
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

'''
Cast image pixels to float, then normalize pixel brightness to scale [0,1], using the maximum value as divisor.
'''
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

'''
Expand the shape of the dataframes to include binary color channel (BW) as the last dimension.
'''
x_train = numpy.expand_dims(x_train, -1)
x_test = numpy.expand_dims(x_test, -1)

'''
Check the shape of the dataframes.
'''
print(f'Train dataframe shape (images, pwidth, pheight, channel): {x_train.shape}')
print(f'Test dataframe shape (images, pwidth, pheight, channel): {x_test.shape}')