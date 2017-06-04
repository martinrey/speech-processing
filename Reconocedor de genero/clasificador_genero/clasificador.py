#!/usr/bin/python3

import os
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import xgboost

import arff


def generar_mfccs():
    for root, subdir, files in os.walk('/home/mcaravario/Escritorio/clasificador/audios'):
        for sound in files:
            output = str(sound[:-4]) + ".arff"
            os.system("/home/mcaravario/Escritorio/clasificador/opensmile/bin/linux_x64_standalone_static/SMILExtract -C " +
            "/home/mcaravario/Escritorio/clasificador/opensmile/config/IS10_paraling.conf -I audios/" + str(sound) + " -O mfccs/" + str(output))


def main():
    x = []
    y = []

    for root, subdir, files in os.walk('/home/mcaravario/Escritorio/clasificador/mfccs'):
        for mfcc in files:
            data = arff.load(open('mfccs/'+ str(mfcc)))
            x.append(np.array(data["data"][0]))
            y.append(0 if mfcc[3] == "m" else 1)

    x = np.array(x)
    y = np.array(y)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Limpio los datos
    for i in range(x_train.shape[0]):
        for j in range(x_train.shape[1]):
            x_train[i][j] = 0.0 if str(x_train[i][j]) == "None" or str(x_train[i][j]) == "unknown" else float(x_train[i][j])

    for i in range(x_test.shape[0]):
        for j in range(x_test.shape[1]):
            x_test[i][j] = 0.0 if str(x_test[i][j]) == "None" or str(x_test[i][j]) == "unknown" else float(x_test[i][j])


    # Normalizacion de los datos
    pca = PCA(n_components=2)
    pca.fit(x_train)

    # mean = x_test.mean(axis=0)
    # std_dev = np.std(x_test, axis=0, dtype=np.float32)
    #
    #
    #
    # for i in range(x_train.shape[0]):
    #     for j in range(x_train.shape[1]):
    #         x_train[i][j] = (x_train[i][j] - mean[j]) / std_dev[j] if x_train[i][j] != 0.0 and std_dev[j] != 0.0 else 0.0


    # Training
    clf = xgboost.XGBClassifier(n_estimators=70, learning_rate=0.04)
    # clf = svm.SVC(kernel='linear', C=0.25)
    # clf = RandomForestClassifier(n_estimators=100)
    scores = cross_val_score(clf, x_train, y_train, cv=3)
    print("Mean accuracy for training: %.2f%%" % (np.mean(scores)*100.0))
    clf.fit(x_train, y_train)

    # xgboost.plot_tree(clf)
    # plt.show()


    # Testing
    y_pred = clf.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy for testing: %.2f%%" % (accuracy * 100.0))


main()
