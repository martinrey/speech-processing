import os
import wav
import numpy as np
import tensorflow as tf
from sklearn.decomposition import PCA
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score, KFold, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.linear_model import SGDClassifier
from sklearn.utils import shuffle
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.layers import Convolution1D, MaxPooling1D, Dropout, Flatten
from keras.datasets import imdb
from sklearn.base import BaseEstimator


class Reshape(BaseEstimator):
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        return X.reshape((150, 32, 1))


def create_model(optimizer='rmsprop', init='glorot_uniform'):
    # CREO MIS CONVOLUCIONES
    model = Sequential()
    model.add(Convolution1D(16, 3, kernel_initializer=init, activation='relu', input_shape=(32, 1)))
    model.add(Convolution1D(32, 3, kernel_initializer=init, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, kernel_initializer=init, activation='relu'))
    model.add(Dense(64, kernel_initializer=init, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model


def main():
    RUTA_DIRECTORIO_DATOS = "datos"
    VENTANA_EN_SEGUNDOS = 10
    SAMPLE_RATE = 16000
    CANTIDAD_DE_FRAMES_A_PROCESAR = 131072

    archivos_en_carpeta_datos = os.listdir(RUTA_DIRECTORIO_DATOS)
    archivos_wav = []
    archivos_ipu = []
    for archivo in archivos_en_carpeta_datos:
        if (archivo[-3:] == "ipu"):
            archivos_ipu.append(archivo)
        elif (archivo[-3:] == "wav"):
            archivos_wav.append(archivo)

    X = []
    for archivo_wav in archivos_wav:
        data, frames, _, duration = wav.load_from_wav(RUTA_DIRECTORIO_DATOS + "/" + archivo_wav)
        X.append(data[:CANTIDAD_DE_FRAMES_A_PROCESAR])

    X = np.asarray(X)

    y = []
    for archivo_wav in archivos_wav:
        if archivo_wav[3] == "m":
            y.append(1)
        elif archivo_wav[3] == "f":
            y.append(0)
    y = np.asarray(y)


    X, y = shuffle(X, y, random_state=0)
    X_train = X[:150]
    X_test = X[150:180]
    y_train = y[:150]
    y_test = y[150:180]

    N_COMPONENTS = [32]
    OPTIMIZERS = ['adam']
    EPOCHS = [100]
    BATCHES = [10]
    INIT = ['glorot_uniform']

    # create model
    model = KerasClassifier(build_fn=create_model, verbose=0)

    estimators = [("reduce_dim", PCA(n_components=32)), ("reshaper", Reshape()), ('clf', model)]
    pipeline = Pipeline(estimators)

    pipeline.fit(X_train, y_train)
    score = pipeline.score(X_train, y_train)
    print(score)
main()


