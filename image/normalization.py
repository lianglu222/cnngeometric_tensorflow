import tensorflow as tf

class NormalizeImageDict(object):
    def __init__(self, image_keys, normalizeRange=True):
        self.image_keys = image_keys
        self.normalizeRange = normalizeRange

    def __call__(self, sample):
        for key in self.image_keys:
            if self.normalizeRange:
                sample[key] /= 255.0
            sample[key] = tf.image.per_image_standardization(sample[key])

        return sample

def normalize_image(image, forward=True, mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225]):
    im_size = tf.shape(image)
    mean = tf.Variable(initial_value=mean, dtype=tf.float32)
    mean = tf.expand_dims(tf.expand_dims(mean, dim=1), dim=2)
    std = tf.Variable(initial_value=std, dtype=tf.float32)
    std = tf.expand_dims(tf.expand_dims(std, dim=1), dim=2)

    if isinstance(image, tf.Variable):
        mean = tf.Variable(mean, trainable=False)
        std = tf.Variable(std, trainable=False)
    if forward:
        if len(im_size) == 3:
            result = tf.subtract(image,tf.divide(tf.tile(mean,im_size), tf.tile(std, im_size)))
        elif len(im_size) == 4:
            result = tf.subtract(image,tf.divide(tf.tile(tf.expand_dims(mean,0),im_size), tf.tile(tf.expand_dims(std,0), im_size)))
    else:
        if len(im_size) == 3:
            result = tf.multiply(image,tf.add(tf.tile(mean,im_size), tf.tile(std, im_size)))
        elif len(im_size) == 4:
            result = tf.multiply(image,tf.add(tf.tile(tf.expand_dims(mean,0),im_size), tf.tile(tf.expand_dims(std,0), im_size)))

    return result