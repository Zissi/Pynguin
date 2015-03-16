'''
Created on 07.03.2015

@author: zissi
'''
import numpy as np
from collections import Counter
from vlfeat import vl_sift, vl_ikmeans, vl_rgb2gray
import Image

def euclidean(a, b):
    return np.linalg.norm(a - b)

class SiftFeatureExtractor(object):
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
        for image in images:
            descriptor = self._get_descriptor(image)
            image_descriptors.append(descriptor)
        return image_descriptors

    def _get_descriptor(self, image, plot=False, pil=False):
        if pil:
            image_grey = image.convert('F')
            image_grey = np.array(image_grey)
        else:
            image_grey = np.array(image)
            image_grey = vl_rgb2gray(image_grey)
        keypoints, descriptor = vl_sift(image_grey)
        if plot:
            xs = keypoints[0].tolist()
            ys = keypoints[1].tolist()
            for x, y in zip(xs, ys):
                x = int(np.round(x))
                y = int(np.round(y))
                image_grey[y - 2:y + 2, x - 2:x + 2] = 255.
            Image.fromarray(image_grey).show()
        return descriptor

    def _make_bag_of_visual_words(self, descriptors, clusters=100):
        descriptors_array = np.hstack(descriptors)
        cluster_centers, assignments = vl_ikmeans(descriptors_array, clusters)
        return cluster_centers

    def _calculate_features(self, descriptors, vocabulary):
        '''translates descriptors of each image into feature vector using the vocabulary'''
        feature_list = []
        for descriptor in descriptors:
            matches = self._find_matches(descriptor, vocabulary)
            feature = np.zeros(len(vocabulary), dtype=int)
            visual_word_counts = Counter(matches)
            for visual_word_idx in visual_word_counts:
                feature[visual_word_idx] = visual_word_counts[visual_word_idx] # adds counts to feature list, to get zeros for not present visual words
            feature_list.append(feature)
        features = np.vstack(feature_list)
        return features

    def _find_matches(self, descriptor, vocabulary, dist_measure=euclidean):
        matches = []
        for entry in np.swapaxes(descriptor, 0, 1):
            best_idx = -1
            best_dist = float("inf")
            for idx, word in enumerate(np.swapaxes(vocabulary, 0, 1)):
                print entry.shape
                print word.shape
                dist = dist_measure(entry, word)
                if dist < best_dist:
                    best_dist = dist
                    best_idx = idx
            matches.append(best_idx)
        return matches

class QuerySiftFeatureExtractor(SiftFeatureExtractor):
    def __init__(self, images, vocabulary):
        self.images = images
        self.vocabulary = vocabulary

    def extract_features(self):
        descriptors = self._calculate_descriptors(self.images)
        features = self._calculate_features(descriptors, self.vocabulary)
        return features

