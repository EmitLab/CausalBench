import tensorflow as tf
import numpy as np
import argparse
import IPython.display as display
import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils import shuffle
import pandas as pd
tf.compat.v1.enable_eager_execution()
import cProfile
from sklearn.model_selection import train_test_split
import copy as cp
from sklearn.model_selection import KFold
from datetime import date
import time

from .OoD.ERMIRM.data_construct import *
from .OoD.ERMIRM.IRM_methods import *

#TODO: How do we process and import the paths if we want to access them from their
# unzipped locations?

def execute(data, space):
    # check if `data` is dataframe
    if not isinstance(data, pd.DataFrame):
        raise TypeError("train data must be a DataFrame object")

    '''
    if not isinstance(test, pd.DataFrame):
        raise TypeError("test data must be a DataFrame object")
    '''

    # the model does not take space, it should be type none.
    if not isinstance(space, None):
        raise TypeError("This model does not support space.")

    ### Model code

    '''
    #Temp data generation.
    
    n_trial =10
    n_tr = 100 # list of training sample sizes
    n_e = 2
    p_color_list = [0.2, 0.1]
    p_label_list = [0.25] * n_e
    D = assemble_data_mnist_confounded(n_tr)  # initialize confounded colored mnist digits data object

    D.create_training_data(n_e, p_color_list, p_label_list)  # creates the training environments

    p_label_test = 0.25  # probability of switching pre-label in test environment
    p_color_test = 0.9  # probability of switching the final label to obtain the color index in test environment

    D.create_testing_data(p_color_test, p_label_test, n_e)  # sets up the testing environment
    '''
    (num_examples_environment, length, width, height) = data.shape  # attributes of the data
    num_classes = len(np.unique(data))  # number of classes in the data

    model_erm = keras.Sequential([
        keras.layers.Flatten(input_shape=(length, width, height)),
        keras.layers.Dense(390, activation='relu', kernel_regularizer=keras.regularizers.l2(0.0011)),
        keras.layers.Dense(390, activation='relu', kernel_regularizer=keras.regularizers.l2(0.0011)),
        keras.layers.Dense(2, activation='softmax')
    ])

    num_epochs = 10
    batch_size = 64
    learning_rate = 4.9e-4
    erm_model1 = standard_erm_model(model_erm, num_epochs, batch_size, learning_rate)
    erm_model1.fit(data)
    preds = erm_model1.evaluate(data.test)

    ###

    result = preds

    # check if returned data type is graph/adjacency matrix
    if isinstance(result, np.ndarray) or isinstance(result, pd.DataFrame):
        # Check if it's a square matrix for adjacency matrix
        if len(result.shape) == 2 and result.shape[0] == result.shape[1]:
            print("result is an adjacency matrix")
        else:
            print("result is not an adjacency matrix")
    else:
        print("result is neither a numpy array nor a pandas DataFrame")


    return (result)