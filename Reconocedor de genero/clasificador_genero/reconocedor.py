#!/usr/bin/python3

import os
import sys
import numpy as np
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import xgboost

import arff


def main():
    x = []
    y = []

    # Extraer mfcc del audio
    audio = sys.argv[1]
    output = str(audio[:-4]) + ".arff"
    os.system("/home/mcaravario/Escritorio/clasificador/opensmile/bin/linux_x64_standalone_static/SMILExtract -C " +
    "/home/mcaravario/Escritorio/clasificador/opensmile/config/IS10_paraling.conf -I " + str(audio) + " -O " + str(output))


    data = arff.load(open(str(output)))

    x_test = np.array(data["data"][0])

    for i in range(x_test.shape[0]):
        x_test[i] = 0.0 if str(x_test[i]) == "None" or str(x_test[i]) == "unknown" else float(x_test[i])



    clf = joblib.load('model.pkl')

    (x_test)

    y_pred = clf.predict(x)

    if(y_pred == 0):
        print("m")
    else:
        print("f")

main()
