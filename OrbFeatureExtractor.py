'''
Created on 07.03.2015

@author: zissi
'''
import cv2
import numpy as np
from collections import Counter
from matplotlib import pyplot as plt

class OrbFeatureExtractor(object):
    '''
    Needs a list of images of equal size.
    '''

    def __init__(self, penguin_images, bird_images):
        self.penguin_images = penguin_images
        self.bird_images = bird_images
        self.vocabulary = None
        
    def extract_features(self):
        penguin_descriptors = self._calculate_descriptors(self.penguin_images)
        bird_descriptors = self._calculate_descriptors(self.bird_images)
        self.vocabulary = self._make_bag_of_visual_words(penguin_descriptors + bird_descriptors)
        penguin_features = self._calculate_features(penguin_descriptors, self.vocabulary)
        bird_features = self._calculate_features(penguin_descriptors, self.vocabulary)
        return penguin_features, bird_features
     
    def _calculate_descriptors(self, images):
        '''extracts keypoints and descriptors from images.'''
        image_descriptors = []
        orb = cv2.ORB_create()
        for image in images:
            descriptor = self._get_descriptor(image, orb)
            image_descriptors.append(descriptor)
        return image_descriptors
    
    def _get_descriptor(self, image, orb):
        image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # orb needs greyscale
        keypoints = orb.detect(image_grey)
        keypoints, descriptor = orb.compute(image_grey, keypoints)
        return descriptor
       
    def _make_bag_of_visual_words(self, descriptors):
        '''creates codebook with 100 clusters'''
        bow_trainer = cv2.BOWKMeansTrainer(100)
        descriptors_array = np.vstack(descriptors)
        bow_trainer.add(descriptors_array)
        return bow_trainer.cluster()  # returns vocabulary as array of floats
        
    def _calculate_features(self, descriptors, vocabulary):
        '''translates descriptors of each image into feature vector using the vocabulary'''
        feature_list = []
        vocabulary = vocabulary.astype("uint8")  # BFMatcher needs ints
        matcher = cv2.BFMatcher()
        for descriptor in descriptors:
            matches = matcher.match(descriptor, vocabulary)  # np.array of match objects between image descriptors and vocabulary
            feature = np.zeros(len(vocabulary), dtype=int)
            visual_word_counts = Counter([x.trainIdx for x in matches])
            for visual_word_idx in visual_word_counts:
                feature[visual_word_idx] = visual_word_counts[visual_word_idx]  # adds counts to feature list, to get zeros for not present visual words
            feature_list.append(feature)
        features = np.vstack(feature_list)         
        return features

class QueryOrbFeatureExtractor(OrbFeatureExtractor):
    def __init__(self, images, vocabulary):
        self.images = images
        self.vocabulary = vocabulary
        
    def extract_features(self):
        descriptors = self._calculate_descriptors(self.images)
        features = self._calculate_features(descriptors, self.vocabulary)
        return features
    
