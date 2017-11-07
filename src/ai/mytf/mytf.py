import numpy as np
import tensorflow as tf
import random

# reproducible
np.random.seed(1)
tf.set_random_seed(1)


class PG1():
    def __init__(self, actions, learningRate=0.002, rewardDecay=0.999):
        self.actions = actions
        self.lr = learningRate
        self.sess = tf.Session()

        self.init = tf.global_variables_initializer()
        self.sess.run(self.init)

    def _buildNet(self):
        layers = []
        layers.append(
            tf.layer.dense(

            )
        )
