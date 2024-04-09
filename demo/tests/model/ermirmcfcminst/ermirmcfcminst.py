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

from OoD.ERMIRM.data_construct import * ## contains functions for constructing data
from OoD.ERMIRM.IRM_methods import *    ## contains IRM and ERM methods

#TODO: How do we process and import the paths if we want to access them from their
# unzipped locations?

def execute(data, space=None):
    # check if `data` is dataframe
    if not isinstance(data.data, pd.DataFrame):
        raise TypeError("data must be a DataFrame object")

    # the model does not take space, it should be type none.
    if not isinstance(space, None):
        raise TypeError("This model does not support space.")

    X = data.data

    ### Model code

    n_trial = 10
    n_tr_list = [100, 500, 1000]  # list of training sample sizes

    k = 0
    K = len(n_tr_list)
    ERM_model_acc = np.zeros((K, n_trial))
    ERM_model_acc_nb = np.zeros((K, n_trial))
    IRM_model_acc = np.zeros((K, n_trial))
    IRM_model_acc_v = np.zeros((K, n_trial))

    ERM_model_acc1 = np.zeros((K, n_trial))
    ERM_model_acc1_nb = np.zeros((K, n_trial))
    IRM_model_acc1 = np.zeros((K, n_trial))
    IRM_model_acc1_v = np.zeros((K, n_trial))
    IRM_model_ind_v = np.zeros((K, n_trial))

    ERM_model_acc_av = np.zeros(K)
    ERM_model_acc_av_nb = np.zeros(K)
    IRM_model_acc_av = np.zeros(K)
    IRM_model_acc_av_v = np.zeros(K)

    ERM_model_acc_av1 = np.zeros(K)
    ERM_model_acc_av1_nb = np.zeros(K)
    IRM_model_acc_av1 = np.zeros(K)
    IRM_model_acc_av1_v = np.zeros(K)

    list_params = []
    for n_tr in n_tr_list:
        print("tr" + str(n_tr))
        #     print ("start")
        t_start = time.time()
        for trial in range(n_trial):
            print("trial " + str(trial))
            n_e = 2
            p_color_list = [0.2, 0.1]
            p_label_list = [0.25] * n_e
            D = assemble_data_mnist_confounded(n_tr)  # initialize confounded colored mnist digits data object

            D.create_training_data(n_e, p_color_list, p_label_list)  # creates the training environments

            p_label_test = 0.25  # probability of switching pre-label in test environment
            p_color_test = 0.9  # probability of switching the final label to obtain the color index in test environment

            D.create_testing_data(p_color_test, p_label_test, n_e)  # sets up the testing environment
            (num_examples_environment, length, width, height) = D.data_tuple_list[0][0].shape  # attributes of the data
            num_classes = len(np.unique(D.data_tuple_list[0][1]))  # number of classes in the data

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
            erm_model1.fit(D.data_tuple_list)
            erm_model1.evaluate(D.data_tuple_test)
            print("Training accuracy:" + str(erm_model1.train_acc))
            print("Testing accuracy:" + str(erm_model1.test_acc))

            ERM_model_acc[k][trial] = erm_model1.test_acc
            ERM_model_acc1[k][trial] = erm_model1.train_acc

            gamma_list = [1000, 3300, 6600]
            index = 0
            best_err = 1e6
            train_list = []
            val_list = []
            test_list = []
            for gamma_new in gamma_list:

                model_irm = keras.Sequential([
                    keras.layers.Flatten(input_shape=(length, width, height)),
                    keras.layers.Dense(390, activation='relu', kernel_regularizer=keras.regularizers.l2(0.0011)),
                    keras.layers.Dense(390, activation='relu', kernel_regularizer=keras.regularizers.l2(0.0011)),
                    keras.layers.Dense(num_classes)
                ])
                batch_size = 64
                steps_max = 100
                steps_threshold = 19  ## threshold after which gamma_new is used
                learning_rate = 4.9e-4

                irm_model1 = irm_model(model_irm, learning_rate, batch_size, steps_max, steps_threshold, gamma_new)
                irm_model1.fit(D.data_tuple_list)
                irm_model1.evaluate(D.data_tuple_test)
                error_val = 1 - irm_model1.val_acc
                train_list.append(irm_model1.train_acc)
                val_list.append(irm_model1.val_acc)
                test_list.append(irm_model1.test_acc)
                if (error_val < best_err):
                    index_best = index
                    best_err = error_val
                index = index + 1

            print("Training accuracy:" + str(train_list[index_best]))
            print("Validation accuracy:" + str(val_list[index_best]))
            print("Testing accuracy:" + str(test_list[index_best]))

            IRM_model_acc_v[k][trial] = test_list[index_best]
            IRM_model_acc1_v[k][trial] = train_list[index_best]
            IRM_model_ind_v[k][trial] = index_best

        IRM_model_acc_av_v[k] = np.mean(IRM_model_acc_v[k])
        list_params.append([n_tr, "IRMv_test", np.mean(IRM_model_acc_v[k]), np.std(IRM_model_acc_v[k])])

        ERM_model_acc_av[k] = np.mean(ERM_model_acc[k])
        list_params.append([n_tr, "ERM_test", np.mean(ERM_model_acc[k]), np.std(ERM_model_acc[k])])

        IRM_model_acc_av1_v[k] = np.mean(IRM_model_acc1_v[k])
        list_params.append([n_tr, "IRMv_train", np.mean(IRM_model_acc1_v[k]), np.std(IRM_model_acc1_v[k])])

        ERM_model_acc_av1[k] = np.mean(ERM_model_acc1[k])
        list_params.append([n_tr, "ERM_train", np.mean(ERM_model_acc1[k]), np.std(ERM_model_acc1[k])])

        k = k + 1

        t_end = time.time()
        print("total time: " + str(t_end - t_start))

    ideal_error = np.ones(5) * 0.25
    results = pd.DataFrame(list_params, columns=["Sample", "Method", "Performance", "Sdev"])

    ###

    result = results
    #pred_output = result['graph']
    #p_matrix = result['p_matrix']

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