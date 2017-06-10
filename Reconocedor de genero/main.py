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
from keras.optimizers import SGD
from sklearn.base import BaseEstimator


class Reshape(BaseEstimator):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return X.reshape((X.shape[0], X.shape[1], 1))


def create_model(learning_rate=0.01, momentum=0, init='glorot_uniform'):
    # CREO MIS CONVOLUCIONES
    model = Sequential()
    model.add(Convolution1D(8, 5, strides=1, padding='same', kernel_initializer=init, activation='relu',
                            input_shape=(64000, 1)))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Convolution1D(16, 5, strides=1, padding='same', kernel_initializer=init, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Convolution1D(32, 5, strides=1, padding='same', kernel_initializer=init, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Convolution1D(64, 5, strides=1, padding='same', kernel_initializer=init, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Convolution1D(128, 5, strides=1, padding='same', kernel_initializer=init, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(256, kernel_initializer=init, activation='relu'))
    model.add(Dense(256, kernel_initializer=init, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    # Compile model
    optimizer = SGD(lr=learning_rate, momentum=momentum)
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model


def main():
    RUTA_DIRECTORIO_DATOS = "datos"
    VENTANA_EN_SEGUNDOS = 4
    SAMPLE_RATE = 16000
    MINIMA_CANTIDAD_DE_FRAMES = 318764  # Es el minimo de todos en este caso
    #CANTIDAD_DE_FRAMES_A_PROCESAR = VENTANA_EN_SEGUNDOS * SAMPLE_RATE
    CANTIDAD_DE_FRAMES_A_PROCESAR = 17303

    def augument_data(dataset, labels):
        augumented_dataset = []
        augumented_labels = []

        for data, label in zip(dataset, labels):
            lower_bound = 0
            upper_bound = CANTIDAD_DE_FRAMES_A_PROCESAR
            augumented_data = []
            # corto en 4 pedazos el audio
            for i in range(4):
                augumented_data.append(data[lower_bound:upper_bound])
                augumented_labels.append(label)
                lower_bound = upper_bound
                upper_bound += CANTIDAD_DE_FRAMES_A_PROCESAR
            augumented_dataset.extend(augumented_data)

        augumented_dataset = np.asarray(augumented_dataset)
        augumented_labels = np.asarray(augumented_labels)
        return augumented_dataset, augumented_labels

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
        X.append(data[:MINIMA_CANTIDAD_DE_FRAMES])

    X = np.asarray(X)

    y = []
    for archivo_wav in archivos_wav:
        if archivo_wav[3] == "m":
            y.append(1)
        elif archivo_wav[3] == "f":
            y.append(0)
    y = np.asarray(y)

    X, y = shuffle(X, y, random_state=42)
    #X_train = X[:150]
    #X_test = X[150:180]
    #y_train = y[:150]
    #y_test = y[150:180]

    X, y = augument_data(X, y)

    #LEARNING_RATE = [0.0001, 0.001, 0.01, 0.1]
    #MOMENTUM = [0.5, 0.7, 0.9]
    #EPOCHS = [1000]
    #BATCHES = [10, 20]
    #INIT = ['glorot_uniform']

    LEARNING_RATE = [0.0001]
    MOMENTUM = [0.7]
    EPOCHS = [2000]
    BATCHES = [20]
    INIT = ['glorot_uniform']

    # pca = PCA(n_components=32)
    # wtf = pca.fit_transform(X_train)

    # create model
    model = KerasClassifier(build_fn=create_model)
    estimators = [("reshaper", Reshape()), ('clf', model)]
    pipeline = Pipeline(estimators)

    param_grid = [
        {
            'clf__epochs': EPOCHS,
            'clf__batch_size': BATCHES,
            'clf__init': INIT,
            'clf__momentum': MOMENTUM,
            'clf__learning_rate': LEARNING_RATE,
        },
    ]

    #kfold = KFold(n_splits=5, shuffle=True)

    grid_search = GridSearchCV(estimator=pipeline, cv=None, param_grid=param_grid)
    grid_result = grid_search.fit(X, y)
    # summarize results
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    grid_search.best_estimator_.named_steps['clf'].model.save('model.h5')
    grid_search.best_estimator_.named_steps['clf'].model.save_weights('model_weights.h5')
main()
