'''
Created on 07.03.2015

@author: zissi
'''
import cv2
import cv2.SURF

class SurfFeatureExtractor(object):
    '''
    classdocs
    '''


    def __init__(self, images):
        self.images = images
     
    def extract(self):
        for image in self.images:
            image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            surf = cv2.SURF()
            kp, descritors = surf.detect(imgg, None, useProvidedKeypoints=False)  
