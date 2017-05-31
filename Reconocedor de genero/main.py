import numpy as np
import tensorflow as tf
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split


class ConvolutionalNeuralNetwork(object):
    def __init__(self, training_set, validation_set, test_set, training_labels,
                 validation_labels, test_labels, training_set_len, num_labels,
                 num_channels, image_size, batch_size, patch_size):

        self.training_set = training_set
        self.validation_set = validation_set
        self.test_set = test_set
        self.training_labels = training_labels
        self.validation_labels = validation_labels
        self.test_labels = test_labels
        self.training_set_len = training_set_len
        self.num_labels = num_labels
        self.num_channels = num_channels
        self.image_size = image_size
        self.batch_size = batch_size
        self.patch_size = patch_size

    # HAY QUE REDEFINIRLA PARA MULTILABEL
    def _accuracy(self, predictions, labels):
        return (100.0 * np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1))
                / predictions.shape[0])

    def train(self):
        # Define the network graph
        graph = tf.Graph()
        with graph.as_default():
            # Input data
            tf_train_dataset = tf.placeholder(
                tf.float32, shape=(self.batch_size, self.image_size, self.num_channels))
            tf_train_labels = tf.placeholder(tf.float32, shape=(self.batch_size, self.num_labels))
            tf_valid_dataset = tf.constant(self.validation_set)
            # tf_test_dataset = tf.constant(self.test_set)

            # Convolution variables
            # [filter_width, in_channels, out_channels],
            layer1_weights = tf.Variable(tf.truncated_normal(
                [self.patch_size, self.num_channels, 16], stddev=0.1))
            layer1_biases = tf.Variable(tf.zeros([16]))
            layer2_weights = tf.Variable(tf.truncated_normal(
                [self.patch_size, 16, 32], stddev=0.1))
            layer2_biases = tf.Variable(tf.zeros([32]))
            layer3_weights = tf.Variable(tf.truncated_normal(
                [self.patch_size, 32, 64], stddev=0.1))
            layer3_biases = tf.Variable(tf.zeros([64]))
            layer4_weights = tf.Variable(tf.truncated_normal(
                [self.patch_size, 64, 128], stddev=0.1))
            layer4_biases = tf.Variable(tf.constant(1.0, shape=[128]))
            layer5_weights = tf.Variable(tf.truncated_normal(
                [self.patch_size, 128, 256], stddev=0.1))
            layer5_biases = tf.Variable(tf.zeros([256]))
            layer6_weights = tf.Variable(tf.truncated_normal(
                [self.patch_size, 256, 512], stddev=0.1))
            layer6_biases = tf.Variable(tf.zeros([512]))
            layer7_weights = tf.Variable(tf.truncated_normal(
                [self.patch_size, 512, 1024], stddev=0.1))
            layer7_biases = tf.Variable(tf.zeros([1024]))
            layer8_weights = tf.Variable(tf.truncated_normal(
                [self.patch_size, 1024, 2048], stddev=0.1))
            layer8_biases = tf.Variable(tf.constant(1.0, shape=[2048]))
            layer9_weights = tf.Variable(tf.truncated_normal(
                [self.patch_size, 2048, 4096], stddev=0.1))
            layer9_biases = tf.Variable(tf.zeros([4096]))
            layer10_weights = tf.Variable(tf.truncated_normal(
                [self.patch_size, 4096, 8192], stddev=0.1))
            layer10_biases = tf.Variable(tf.zeros([8192]))

            # DNN variables
            layer14_weights = tf.Variable(tf.truncated_normal(
                [32 * 8192, 2048], stddev=0.1))
            layer14_biases = tf.Variable(tf.constant(1.0, shape=[2048]))
            layer15_weights = tf.Variable(tf.truncated_normal(
                [2048, 2048], stddev=0.1))
            layer15_biases = tf.Variable(tf.constant(1.0, shape=[2048]))
            layer16_weights = tf.Variable(tf.truncated_normal(
                [2048, self.num_labels], stddev=0.1))
            layer16_biases = tf.Variable(tf.constant(1.0, shape=[self.num_labels]))

            def model(data):
                # Convolutions
                conv = tf.nn.conv1d(data, layer1_weights, 2, padding='SAME')
                hidden = tf.nn.relu(conv + layer1_biases)
                conv = tf.nn.conv1d(hidden, layer2_weights, 2, padding='SAME')
                hidden = tf.nn.relu(conv + layer2_biases)
                conv = tf.nn.conv1d(hidden, layer3_weights, 2, padding='SAME')
                hidden = tf.nn.relu(conv + layer3_biases)
                conv = tf.nn.conv1d(hidden, layer4_weights, 2, padding='SAME')
                hidden = tf.nn.relu(conv + layer4_biases)
                conv = tf.nn.conv1d(hidden, layer5_weights, 2, padding='SAME')
                hidden = tf.nn.relu(conv + layer5_biases)
                conv = tf.nn.conv1d(hidden, layer6_weights, 2, padding='SAME')
                hidden = tf.nn.relu(conv + layer6_biases)
                conv = tf.nn.conv1d(hidden, layer7_weights, 2, padding='SAME')
                hidden = tf.nn.relu(conv + layer7_biases)
                conv = tf.nn.conv1d(hidden, layer8_weights, 2, padding='SAME')
                hidden = tf.nn.relu(conv + layer8_biases)
                conv = tf.nn.conv1d(hidden, layer9_weights, 2, padding='SAME')
                hidden = tf.nn.relu(conv + layer9_biases)
                conv = tf.nn.conv1d(hidden, layer10_weights, 2, padding='SAME')
                hidden = tf.nn.relu(conv + layer10_biases)

                # DNN
                shape = hidden.get_shape().as_list()
                reshape = tf.reshape(hidden, [shape[0], shape[1] * shape[2]])
                hidden = tf.nn.relu(tf.matmul(reshape, layer14_weights) + layer14_biases)
                hidden = tf.nn.relu(tf.matmul(hidden, layer15_weights) + layer15_biases)
                return tf.matmul(hidden, layer16_weights) + layer16_biases

            # Training computation.
            logits = model(tf_train_dataset)
            loss = tf.reduce_mean(
                tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=tf_train_labels))

            # Optimizer.
            optimizer = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

            # Predictions for the training, validation, and test data.
            train_prediction = tf.nn.softmax(logits)
            valid_prediction = tf.nn.softmax(model(tf_valid_dataset))
            # test_prediction = tf.nn.sigmoid(model(tf_test_dataset))

        num_steps = 5000

        with tf.Session(graph=graph) as session:
            tf.global_variables_initializer().run()
            print("Initialized")
            for step in range(num_steps):
                print(step)
                batch_offset = (step * self.batch_size) % (len(self.training_set))
                batch_data = self.training_set[batch_offset:(batch_offset + self.batch_size)]
                batch_labels = self.training_labels[batch_offset:(batch_offset + self.batch_size)]
                batch_data, batch_labels = shuffle(batch_data, batch_labels, random_state=0)

                feed_dict = {tf_train_dataset: batch_data, tf_train_labels: batch_labels}
                _, l, predictions = session.run(
                    [optimizer, loss, train_prediction], feed_dict=feed_dict)
                if (step % 5 == 0):
                    print("Minibatch loss:", l)
                    print("Minibatch accuracy: {:01.2f} at step {}".format(
                        self._accuracy(train_prediction.eval(feed_dict={tf_train_dataset: batch_data}), batch_labels),
                        step))
                    print("Validation accuracy: %.1f%%" % self._accuracy(
                        valid_prediction.eval(), self.validation_labels))


# print("Validation accuracy: {:01.2f}".format(self._accuracy(valid_prediction.eval(),
#                                                                                self.validation_labels_reader.read(
#                                                                                    from_index=0, to_index=1000))))

def main():
    RUTA_DIRECTORIO_DATOS = "../datos"
    VENTANA_EN_SEGUNDOS = 10
    SAMPLE_RATE = 16000
    CANTIDAD_DE_FRAMES_A_PROCESAR = 32768

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

    print(np.shape(y))


    shuffle(X, y, random_state=42)
    X_train = X[:150]
    X_test = X[150:180]
    y_train = y[:150]
    y_test = X[150:180]

    print("Shape X_train {}".format(np.shape(X_train)))
    print("Shape X_test {}".format(np.shape(X_test)))
    print("Shape y_train {}".format(np.shape(y_train)))
    print("Shape y_test {}".format(np.shape(y_test)))

    TRAINING_SET_LEN = len(X_train)
    NUM_CHANNELS = 1
    NUM_LABELS = 2
    BATCH_SIZE = 10
    PATCH_SIZE = 5


    conv_net = ConvolutionalNeuralNetwork(training_set=X_train,
                                          validation_set=X_test,
                                          test_set=[],
                                          training_labels=y_train,
                                          validation_labels=y_test,
                                          test_labels=[], training_set_len=TRAINING_SET_LEN,
                                          num_labels=NUM_LABELS,
                                          num_channels=NUM_CHANNELS,
                                          image_size=CANTIDAD_DE_FRAMES_A_PROCESAR,
                                          batch_size=BATCH_SIZE, patch_size=PATCH_SIZE)

    conv_net.train()


main()