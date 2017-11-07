import numpy as np
import tensorflow as tf
import random

# reproducible
np.random.seed(1)
tf.set_random_seed(1)

class  PG1():
    def __init__(self,actions,learningRate=0.002,rewardDecay=0.995,netDeepth=10):
        self.actions=actions
        self.lr=learningRate
        self.gama=rewardDecay
        self.netDeepth=netDeepth

        self.sess = tf.Session()

        self.boardInfo=None

        self._buildNet()
        self.init=tf.global_variables_initializer()
        self.sess.run(self.init)



    def _buildNet(self):
        with tf.name_scope('inputs'):

            self.tf_acts = tf.placeholder(tf.int32, [None, ], name="actions_num")
            self.tf_vt = tf.placeholder(tf.float32, [len(self.actions), ], name="actions_value")


        layers=[]
        tempLayer=tf.layers.dense(
                inputs=self.boardInfo,
                units=10,
                activation=tf.nn.tanh,  # tanh activation
                kernel_initializer=tf.random_normal_initializer(mean=0, stddev=0.3),
                bias_initializer=tf.constant_initializer(0.1),
                name='layer0'
            )
        layers.append(tempLayer)
        for i in range(1,self.netDeepth):
            t2= tf.layers.dense(
                inputs=tempLayer,
                units=10,
                activation=tf.nn.tanh,  # tanh activation
                kernel_initializer=tf.random_normal_initializer(mean=0, stddev=0.3),
                bias_initializer=tf.constant_initializer(0.1),
                name='layer'+str(i)
            )
            layers.append(t2)
            tempLayer=t2

        self.all_act_prob = tf.nn.softmax(tempLayer, name='act_prob')

        with tf.name_scope('loss'):
            # to maximize total reward (log_p * R) is to minimize -(log_p * R), and the tf only have minimize(loss)
            neg_log_prob = tf.reduce_sum(-tf.log(self.all_act_prob)*tf.one_hot(self.tf_acts, self.n_actions), axis=1)
            loss = tf.reduce_mean(neg_log_prob * self.tf_vt)  # reward guided loss

        with tf.name_scope('train'):
            self.train_op = tf.train.AdamOptimizer(self.lr).minimize(loss)
