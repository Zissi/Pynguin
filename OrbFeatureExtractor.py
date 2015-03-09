'''
Created on 07.03.2015

@author: zissi
'''
import cv2
import numpy as np
from collections import Counter

class OrbFeatureExtractor(object):
    '''
    Needs a list of images of equal size.
    '''

    def __init__(self, images):
        self.images = images
        
    def extract_features(self):
        descriptors = self._calculate_descriptors()
        vocabulary = self._make_bag_of_visual_words(descriptors)
        features = self._calculate_features(descriptors, vocabulary)
        return features
     
    def _calculate_descriptors(self):
        '''extracts keypoints and descriptors from images.'''
        image_descriptors = []
        orb = cv2.ORB_create()
        for image in self.images:
            descriptor = self._get_descriptor(image, orb)
            image_descriptors.append(descriptor)
        return image_descriptors
    
    def _get_descriptor(self, image, orb):
        image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # orb needs greyscale
        keypoints = orb.detect(image_grey)
        _, descriptor = orb.compute(image_grey, keypoints)
        return descriptor
       
    def _make_bag_of_visual_words(self, descriptors):
        '''creates codebook with 500 clusters'''
        bow_trainer = cv2.BOWKMeansTrainer(500)
        descriptors = [descriptor.astype(np.float32) for descriptor in descriptors]  # BOW needs 32bit floats for vocabulary creation
        descriptors_array = np.vstack(descriptors)
        bow_trainer.add(descriptors_array)
        return bow_trainer.cluster()  # returns vocabulary as array of floats
        
    def _calculate_features(self, descriptors, vocabulary):
        '''translates descriptors of each image into feature vector using the vocabulary'''
        features = []
        vocabulary = vocabulary.astype("uint8")  # BFMatcher needs ints
        matcher = cv2.BFMatcher()
        for descriptor in descriptors:
            matches = matcher.match(descriptor, vocabulary)  # np.array of match objects between image descriptors and vocabulary
            feature = np.zeros(len(vocabulary), dtype=int)
            visual_word_counts = Counter([x.trainIdx for x in matches])
            for visual_word_idx in visual_word_counts:
                feature[visual_word_idx] = visual_word_counts[visual_word_idx]  # adds counts to feature list, to get zeros for not present visual words
            features.append(feature)
        return features
