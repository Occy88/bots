import os

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models

from DetectPokestop import clean_img
from ImgTools import load_dir, resize_images


def setup_dataset(im_valid, im_invalid, np_img_dim):
    print("setinug up dataset")
    inv = load_dir(im_invalid, np_img_dim)
    print('invalid: ', inv.shape)
    val = load_dir(im_valid, np_img_dim)
    print('valid:', val.shape)
    inv_l = np.zeros(len(inv))
    val_l = np.ones(len(val))

    X = np.concatenate([inv, val])
    Y = np.concatenate([inv_l, val_l])
    print("DATASET LOADED")
    print(X.shape, Y.shape)

    return X, Y


def preprocess_images(X, resize_dim, clean_function=lambda x: x):
    print('preprocessing')
    X = clean_function(X)
    X = resize_images(X, resize_dim)
    # normalize
    X = X / 255
    return X


def conv2d_32_32_3_model():
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(2))

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    return model


def load_model(model_path):
    return tf.keras.models.load_model(model_path)


def train_images(X, Y, model, save_path):
    # Normalize images
    print("training: ", X.shape, Y.shape)
    xtr, xts, ytr, yts = train_test_split(X, Y, test_size=0.33, random_state=42)

    history = model.fit(xtr, ytr, epochs=10,
                        validation_data=(xts, yts))
    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0.5, 1])
    plt.legend(loc='lower right')
    plt.show()
    test_loss, test_acc = model.evaluate(xts, yts, verbose=2)
    print(test_acc)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    model.save(save_path)
    return model


def train_model(detect_images, ignore_images, img_np_dim, preprocess_function, model_save_path):
    x, y = setup_dataset(detect_images, ignore_images, img_np_dim)
    print("DATASET LOADED")
    print(x.shape)
    print('PREPROCESSING')
    x = preprocess_function(x)
    print("PREPROCESSING FINISHED")
    print(x.shape)
    print('TRAINING')
    return train_images(x, y, conv2d_32_32_3_model(), model_save_path)


def train_pogo_model():
    return train_model('images/Pokestop/*',
                       'images/Nothing/*',
                       (100, 150, 3),
                       lambda X: preprocess_images(X, (32, 32, 3), clean_img),
                       'models/PokestopDetect')


def test_find_img(kx, ky,thresh):
    model = tf.keras.models.load_model('models/PokestopDetect')
    from ImgTools import template_match_tfmodel, load_img, show_img, crop_img_percent, find_peaks
    import cv2
    template = crop_img_percent(load_img('pokestop_detect1.png'), 0, 0, 1, 1)
    print(template)
    cv2.imshow('preview', template)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print('template:', template.shape)

    def preprocess_for_pokestop(X):
        return preprocess_images(X, (32, 32, 3))

    pict = template_match_tfmodel(template, (100, 150, 3), preprocess_for_pokestop, model.predict, kx, ky)
    pict_peaks = find_peaks(pict, thresh)
    show_img(pict)
    show_img(pict_peaks)
    return pict
