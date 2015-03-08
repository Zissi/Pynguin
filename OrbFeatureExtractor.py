'''
Created on 07.03.2015

@author: zissi
'''
import cv2
import Image
import numpy as np
from collections import Counter

class OrbFeatureExtractor(object):
    '''
    classdocs
    '''

    def __init__(self, images):
        self.images = images
        self.image_descriptors = []
     
    def extract(self, show_keypoints=False):
        descriptors = np.ndarray((0, 32))
        for image in self.images:
            image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            orb = cv2.ORB_create()
            keypoints = orb.detect(image_grey)
            keypoints, descriptor = orb.compute(image_grey, keypoints)
            self.image_descriptors.append(descriptor)
            descriptors = np.vstack([descriptors, descriptor])
            if show_keypoints:
                image_new = np.ndarray(image_grey.shape)
                image_new = cv2.drawKeypoints(image_grey, keypoints, image_new)
                Image.fromarray(image_new).show()
        return descriptors.astype(np.float32)

    
    def make_bag_of_visual_words(self):
        bow_trainer = cv2.BOWKMeansTrainer(500)
        bow_trainer.add(self.extract())
        return bow_trainer.cluster()
        
    def get_features(self):
        features = []
        vocabulary = self.make_bag_of_visual_words()
        vocabulary = vocabulary.astype("uint8")
        matcher = cv2.BFMatcher()
        for descriptor in self.image_descriptors:
            matches = matcher.match(descriptor, vocabulary)
            feature = np.zeros(len(vocabulary), dtype=int)
            hits = Counter([x.trainIdx for x in matches])
            for idx in hits:
                feature[idx] = hits[idx]
            features.append(feature)
        return features