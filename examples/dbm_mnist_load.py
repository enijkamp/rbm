import numpy as np
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
#from JSAnimation.IPython_display import display_animation
from sklearn.metrics import accuracy_score, confusion_matrix

import os

# set GPU
GPU = 0
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = str(GPU)

import env
from bm import DBM
from bm.rbm import BernoulliRBM
from bm.utils import (progress_bar, Stopwatch,
                      im_plot, im_reshape, im_gif, tick_params,
                      plot_confusion_matrix)
from bm.utils.dataset import load_mnist


X, y = load_mnist(mode='train', path='../data/')
X /= 255.
X_test, y_test = load_mnist(mode='test', path='../data/')
X_test /= 255.
print(X.shape, y.shape, X_test.shape, y_test.shape)


fig = plt.figure(figsize=(10, 10))
im_plot(X[:100], shape=(28, 28), title='Training examples',
        imshow_params={'cmap': plt.cm.gray})
plt.savefig('mnist.png', dpi=196, bbox_inches='tight')


rbm1 = BernoulliRBM.load_model('../models/dbm_mnist_rbm1/')

rbm1_W = rbm1.get_tf_params(scope='weights')['W']
fig = plt.figure(figsize=(10, 10))
im_plot(rbm1_W.T, shape=(28, 28), title='First 100 filters extracted by RBM #1',
        imshow_params={'cmap': plt.cm.gray});
plt.savefig('dbm_mnist_rbm1.png', dpi=196, bbox_inches='tight');


rbm2 = BernoulliRBM.load_model('../models/dbm_mnist_rbm2/')

rbm2_W = rbm2.get_tf_params(scope='weights')['W']
U = rbm1_W.dot(rbm2_W)

fig = plt.figure(figsize=(10, 10))
im_plot(U.T, shape=(28, 28), title='First 100 (high-level) filters extracted by RBM #2',
        imshow_params={'cmap': plt.cm.gray});
plt.savefig('dbm_mnist_rbm2.png', dpi=196, bbox_inches='tight');



dbm = DBM.load_model('../models/dbm_mnist/')
dbm.load_rbms([rbm1, rbm2])  # !!!


W1_joint = dbm.get_tf_params(scope='weights')['W']

fig = plt.figure(figsize=(10, 10))
im_plot(W1_joint.T, shape=(28, 28), title='First 100 filters of DBM after joint training (1st layer)',
        title_params={'fontsize': 20}, imshow_params={'cmap': plt.cm.gray});
plt.savefig('dbm_mnist_W1_joint.png', dpi=196, bbox_inches='tight');


W2_joint = dbm.get_tf_params(scope='weights')['W_1']
U_joint = W1_joint.dot(W2_joint)

fig = plt.figure(figsize=(10, 10))
im_plot(U_joint.T, shape=(28, 28), title='First 100 filters of DBM after joint training (2nd layer)',
        title_params={'fontsize': 20}, imshow_params={'cmap': plt.cm.gray});
plt.savefig('dbm_mnist_W2_joint.png', dpi=196, bbox_inches='tight');




with Stopwatch(verbose=True) as s:
    V = dbm.sample_v(n_gibbs_steps=1337)

fig = plt.figure(figsize=(10, 10))
im_plot(V, shape=(28, 28), title='Samples generated by DBM after 1337 Gibbs steps',
        imshow_params={'cmap': plt.cm.gray});
plt.savefig('dbm_mnist_samples.png', dpi=196, bbox_inches='tight');


