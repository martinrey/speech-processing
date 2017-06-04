import os
import wav
import numpy as np
import tensorflow as tf
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, ClassifierMixin


class CovNetClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, num_channels, num_labels, image_size, batch_size, patch_size, epochs):
        # PARAMETROS
        self.num_channels = num_channels
        self.num_labels = num_labels
        self.image_size = image_size
        self.batch_size = batch_size
        self.patch_size = patch_size
        self.epochs = epochs

        # PROPIEDADES DE LA RED
        # INICIALIZO EL GRAFO
        self.graph = tf.Graph()
        with self.graph.as_default():
            # Input data
            self.tf_X = tf.placeholder(tf.float32, shape=(self.batch_size, self.image_size, self.num_channels),
                                       name="asd")
            self.tf_y = tf.placeholder(tf.float32, shape=(self.batch_size, self.num_labels), name="dsa")

            conv_weight_layer1 = tf.get_variable("conv_weight_layer1", shape=[self.patch_size, self.num_channels, 16],
                                                 initializer=tf.contrib.layers.xavier_initializer())
            conv_biases_layer1 = tf.Variable(tf.zeros([16]), name="conv_biases_layer1")
            conv_weight_layer2 = tf.get_variable("conv_weight_layer2", shape=[self.patch_size, 16, 32],
                                                 initializer=tf.contrib.layers.xavier_initializer())
            conv_biases_layer2 = tf.Variable(tf.zeros([32]), name="conv_biases_layer2")
            conv_weight_layer3 = tf.get_variable("conv_weight_layer3", shape=[self.patch_size, 32, 64],
                                                 initializer=tf.contrib.layers.xavier_initializer())
            conv_biases_layer3 = tf.Variable(tf.zeros([64]), name="conv_biases_layer3")
            conv_weight_layer4 = tf.get_variable("conv_weight_layer4", shape=[self.patch_size, 64, 128],
                                                 initializer=tf.contrib.layers.xavier_initializer())
            conv_biases_layer4 = tf.Variable(tf.zeros([128]), name="conv_biases_layer4")
            conv_weight_layer5 = tf.get_variable("conv_weight_layer5", shape=[self.patch_size, 128, 256],
                                                 initializer=tf.contrib.layers.xavier_initializer())
            conv_biases_layer5 = tf.Variable(tf.zeros([256]), name="conv_biases_layer5")
            conv_weight_layer6 = tf.get_variable("conv_weight_layer6", shape=[self.patch_size, 256, 512],
                                                 initializer=tf.contrib.layers.xavier_initializer())
            conv_biases_layer6 = tf.Variable(tf.zeros([512]), name="conv_biases_layer6")
            conv_weight_layer7 = tf.get_variable("conv_weight_layer7", shape=[self.patch_size, 512, 1024],
                                                 initializer=tf.contrib.layers.xavier_initializer())
            conv_biases_layer7 = tf.Variable(tf.zeros([1024]), name="conv_biases_layer7")
            conv_weight_layer8 = tf.get_variable("conv_weight_layer8", shape=[self.patch_size, 1024, 2048],
                                                 initializer=tf.contrib.layers.xavier_initializer())
            conv_biases_layer8 = tf.Variable(tf.constant(1.0, shape=[2048]), name="conv_biases_layer8")

            dnn_weight_layer9 = tf.get_variable("dnn_weight_layer9", shape=[512 * 2048, 200],
                                                initializer=tf.contrib.layers.xavier_initializer())
            dnn_biases_layer9 = tf.Variable(tf.constant(1.0, shape=[200]), name="dnn_biases_layer9")
            dnn_weight_layer10 = tf.get_variable("dnn_weight_layer10", shape=[200, 200],
                                                 initializer=tf.contrib.layers.xavier_initializer())
            dnn_biases_layer10 = tf.Variable(tf.constant(1.0, shape=[200]), name="dnn_biases_layer10")
            dnn_weight_layer11 = tf.get_variable("dnn_weight_layer11", shape=[200, self.num_labels],
                                                 initializer=tf.contrib.layers.xavier_initializer())
            dnn_biases_layer11 = tf.Variable(tf.constant(1.0, shape=[self.num_labels]), name="dnn_biases_layer11")

            # Training computation.
            logits = self._model(self.tf_X)

            # Predictions for the training data set
            self.train_prediction = tf.nn.softmax(logits)

            self.loss = tf.reduce_mean(
                tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=self.tf_y))

            # Optimizer.
            self.optimizer = tf.train.GradientDescentOptimizer(1e-4).minimize(self.loss)

    def _model(self, X):
        # OJO QUE SI TENGO SOLO 2 CAPAS ESTO ANDA MAL
        conv = tf.nn.conv1d(X, tf.trainable_variables()[0], 2, padding='SAME')
        hidden = tf.nn.relu(conv + tf.trainable_variables()[1])

        loop_trainable_variables = tf.trainable_variables()[2:-2]
        entre = False
        for weight_layer, bias_layer in zip(loop_trainable_variables[0::2], loop_trainable_variables[1::2]):
            if weight_layer.name[:4] == "conv":
                conv = tf.nn.conv1d(hidden, weight_layer, 2, padding='SAME')
                hidden = tf.nn.relu(conv + bias_layer)
            else:
                if not entre:
                    shape = hidden.get_shape().as_list()
                    reshape = tf.reshape(hidden, [shape[0], shape[1] * shape[2]])
                    hidden = tf.nn.relu(tf.matmul(reshape, weight_layer) + bias_layer)
                    entre = True
                else:
                    hidden = tf.nn.relu(tf.matmul(hidden, weight_layer) + bias_layer)

        last_weight_layer = tf.trainable_variables()[-2]
        last_bias_layer = tf.trainable_variables()[-1]
        return tf.matmul(hidden, last_weight_layer) + last_bias_layer

    def fit(self, X, y):
        session = tf.Session(graph=self.graph)
        tf.global_variables_initializer().run(session=session)
        print("Initialized")
        for step in range(self.epochs):
            batch_offset = (step * self.batch_size) % (len(X))
            batch_data = X[batch_offset:(batch_offset + self.batch_size)]
            batch_labels = y[batch_offset:(batch_offset + self.batch_size)]
            batch_data, batch_labels = shuffle(batch_data, batch_labels, random_state=0)

            feed_dict = {self.tf_X: batch_data, self.tf_y: batch_labels}
            _, l, predictions = session.run(
                [self.optimizer, self.loss, self.train_prediction], feed_dict=feed_dict)
        return self

    def predict(self, X):
        prediction = tf.nn.softmax(self._model(X)).eval(session=session)
        return prediction

    def _accuracy(self, predictions, labels):
        result = (100.0 * np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1)) / predictions.shape[0])
        return result

    def score(self, X, y):
        predictions = self.predict(X)
        score = self._accuracy(predictions=predictions, labels=y)
        return score


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

    def reformat(dataset):
        shape = dataset.shape
        dataset = dataset.reshape(
            (shape[0], shape[1], 1)).astype(np.float32)
        return dataset

    X = reformat(X)
    print(X.shape)

    y = []
    for archivo_wav in archivos_wav:
        if archivo_wav[3] == "m":
            y.append([1, 0])
        elif archivo_wav[3] == "f":
            y.append([0, 1])

    X, y = shuffle(X, y, random_state=0)
    X_train = X[:150]
    X_test = X[150:180]
    y_train = y[:150]
    y_test = y[150:180]
    print("LA CONCHA DE TU MADRE")
    print(X_train.shape)

    print("Shape X_train {}".format(np.shape(X_train)))
    print("Shape X_test {}".format(np.shape(X_test)))
    print("Shape y_train {}".format(np.shape(y_train)))
    print("Shape y_test {}".format(np.shape(y_test)))

    TRAINING_SET_LEN = len(X_train)
    NUM_CHANNELS = 1
    NUM_LABELS = 2
    BATCH_SIZE = 10
    PATCH_SIZE = 10

    conv_net = CovNetClassifier(num_channels=NUM_CHANNELS, num_labels=NUM_LABELS,
                                image_size=CANTIDAD_DE_FRAMES_A_PROCESAR, batch_size=BATCH_SIZE,
                                patch_size=PATCH_SIZE, epochs=2)

    conv_net.fit(X_train, y_train)
    score = conv_net.score(X_test, y_test)
    print(score)


main()
