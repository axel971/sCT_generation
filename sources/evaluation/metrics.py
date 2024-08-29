import numpy as np

def mae(y_pred, y_true):

    return np.mean(np.abs(y_pred - y_true))

def me(y_pred, y_true):

    return np.mean(y_pred - y_true)
