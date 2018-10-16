import pickle
import os


def save(name, val, dir='save'):
    path = '{}/{}.pkl'.format(dir, name)
    with open(path, 'wb') as f:
        pickle.dump(val, f)


def load(name, dir='save', default=None):
    path = '{}/{}.pkl'.format(dir, name)
    if default is not None and not os.path.exists(path):
        return default
    with open(path, 'rb') as f:
        val = pickle.load(f)
    return val
