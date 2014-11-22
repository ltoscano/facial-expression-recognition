from convnet import *
#from util import load_labeled_training, shuffle_in_unison
# had to move the functions into this file because the name util was confounded
import numpy as np
import scipy.io
import pprint
from zca import ZCA

def load_labeled_training(flatten=False):
    labeled = scipy.io.loadmat('../labeled_images.mat')
    labels = labeled['tr_labels']
    labels = np.asarray([l[0] for l in labels])
    images = labeled['tr_images']

    # permute dimensions so that the number of instances is first
    x, y, n = images.shape
    images = np.transpose(images, [2, 0, 1])
    assert images.shape == (n, x, y)

    # flatten the pixel dimensions
    if flatten is True:
        n, x, y = images.shape
        images = images.reshape(images.shape[0], images.shape[1]*images.shape[2])
        assert images.shape == (n, x*y)

    return images, labels

def shuffle_in_unison(a, b):
    """Shuffle two arrays in unison, so that previously aligned indices
    remain aligned. The arrays can be multidimensional; in any
    case, the first dimension is shuffled.
    """
    assert len(a) == len(b)
    rng_state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(rng_state)
    np.random.shuffle(b)

labeled_training, labeled_training_labels = load_labeled_training(flatten=True)

zca = ZCA().fit(labeled_training)
labeled_training = zca.transform(labeled_training)

# dumb validation set partition for now
shuffle_in_unison(labeled_training, labeled_training_labels)
valid_split = labeled_training.shape[0] // 4
train_data, train_labels = (labeled_training[valid_split:, :], labeled_training_labels[valid_split:])
valid_data, valid_labels = (labeled_training[:valid_split, :], labeled_training_labels[:valid_split])

# create phony parameters for debugging
test_params = {
    'number of epochs' : 100,
    'batch size' : 100,
    'filter size' : 3,
    'number of kernels' : '20,30,40',
    'pool size' : 2,
    'learning rate' : 0.08,
    'learning rate decay' : 0.998,
    'convpool layer activation function' : 'tanh',
    'hidden layer activation function' : 'tanh',
    'number of convpool layers' : 1,
    'number of hidden layers' : 1,
    'number of hidden units' : 100
}

def main(job_id, params):
    pprint.pprint(params)
    return evaluate_lenet5(
        initial_learning_rate=params['learning rate'][0],
        learning_rate_decay=params['learning rate decay'][0],
        n_epochs=params['number of epochs'][0],
        nkerns=[int(n) for n in params['number of kernels'][0].split(',')],
        batch_size=params['batch size'][0],
        filter_size = (params['filter size'][0], params['filter size'][0]),
        pool_size = (params['pool size'][0], params['pool size'][0]),
        n_convpool_layers = params['number of convpool layers'][0],
        n_hidden_layers = params['number of hidden layers'][0],
        n_hidden_units = params['number of hidden units'][0],
        convpool_layer_activation=params['convpool layer activation function'][0],
        hidden_layer_activation=params['hidden layer activation function'][0],
        training_data=(train_data, train_labels),
        validation_data=(valid_data, valid_labels)
    )

if __name__ == '__main__':
    main(1601, test_params)
