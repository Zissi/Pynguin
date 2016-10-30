'''
Created on 07.03.2015

@author: zissi
'''
import os
import cv2

class DataCleaner(object):
    '''
    Collects images from image folder and resizes them.
    '''

    def __init__(self, images_folder, max_size=200):
        self.images_folder = images_folder
        self.max_size = max_size
       
    def _resize_image(self, image_path):  
        im = cv2.imread(image_path)
        if im is None:
            raise IOError("Could not read image")
        largest_side = max(im.shape[:-1])
        factor = 1. * self.max_size / largest_side
        small = cv2.resize(im, (0, 0), fx=factor, fy=factor) 
        return small
    
    def collect_and_resize(self):
        resized_images = []
        for image in os.listdir(self.images_folder):
            image_path = os.path.join(self.images_folder, image)
            if os.path.isfile(image_path):
                try:
                    resized_image = self._resize_image(image_path)
                    resized_images.append(resized_image)
                except IOError:
                    continue
        return resized_images
        
    
    
            
