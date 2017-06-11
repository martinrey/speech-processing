import os
import arff

import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
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
                            input_shape=(1584, 1)))
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
    RUTA_DIRECTORIO_DATOS = "mfccs"

    archivos_en_carpeta_datos = os.listdir(RUTA_DIRECTORIO_DATOS)
    archivos_mfcc = []
    for archivo in archivos_en_carpeta_datos:
        archivos_mfcc.append(archivo)

    X = []
    y = []

    for mfcc in archivos_mfcc:
        data = arff.load(open('mfccs/'+ str(mfcc)))
        X.append(np.array(data["data"][0]))
        y.append(0 if mfcc[3] == "m" else 1)

    X = np.array(X)
    y = np.array(y)

    # Limpio los datos
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            X[i][j] = 0.0 if str(X[i][j]) == "None" or str(X[i][j]) == "unknown" else float(X[i][j])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    LEARNING_RATE = [0.0001]
    MOMENTUM = [0.7]
    EPOCHS = [200]
    BATCHES = [20]
    INIT = ['glorot_uniform']

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
    grid_result = grid_search.fit(X_train, y_train)

    # summarize results
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    grid_search.best_estimator_.named_steps['clf'].model.save('model.h5')
    grid_search.best_estimator_.named_steps['clf'].model.save_weights('model_weights.h5')
main()
