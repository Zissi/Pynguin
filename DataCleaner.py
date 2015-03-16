'''
Created on 07.03.2015

@author: zissi
'''
import os
import cv2
import Image

class DataCleaner(object):
    '''
    Collects images from image folder and resizes them.
    '''

    def __init__(self, images_folder, max_size=200, cv=True):
        self.images_folder = images_folder
        self.max_size = max_size
        self.cv = cv

    def _resize_image_cv(self, image_path):
        im = cv2.imread(image_path)
        if im is None:
            return None
        largest_side = max(im.shape[:-1])
        factor = 1. * self.max_size / largest_side
        small = cv2.resize(im, (0, 0), fx=factor, fy=factor)
        return small

    def _resize_image_pil(self, image_path):
        try:
            im = Image.open(image_path)
        except IOError:
            return None
        im.thumbnail((self.max_size, self.max_size), Image.ANTIALIAS)
        return im

    def _resize_image(self, image_path):
        if self.cv:
            return self._resize_image_cv(image_path)
        else:
            return self._resize_image_pil(image_path)

    def collect_and_resize(self):
        resized_images = []
        for image in os.listdir(self.images_folder):
            image_path = os.path.join(self.images_folder, image)
            if not os.path.isfile(image_path):
                continue
            resized_image = self._resize_image(image_path)
            if resized_image is None:
                continue
            resized_images.append(resized_image)
        return resized_images




