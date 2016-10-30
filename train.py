'''
Created on 07.03.2015

@author: zissi
'''

import os
import pickle

from Classificator import Classificator
from DataCleaner import DataCleaner
from RgbHistogramExtractor import RgbHistogramExtractor


def cross_validate(path_birds, path_penguins, classifier_type):
    pkl_path = '{}.pkl'.format(hash(path_birds + path_penguins))
    if os.path.exists(pkl_path):
        with open(pkl_path) as pkl_file:
            bird_histogramms, penguin_histogramms = pickle.load(pkl_file)

    else:
        data_cleaner = DataCleaner(path_birds)
        clean_birds = data_cleaner.collect_and_resize()

        data_cleaner.images_folder = path_penguins
        clean_penguins = data_cleaner.collect_and_resize()

        hist = RgbHistogramExtractor(clean_birds)
        bird_histogramms = hist.calc_hist()
        hist.images = clean_penguins
        penguin_histogramms = hist.calc_hist()

        with open(pkl_path, 'wb') as pkl_file:
            pickle.dump((bird_histogramms, penguin_histogramms), pkl_file, pickle.HIGHEST_PROTOCOL)

    clf = Classificator(penguin_histogramms, bird_histogramms)
    print clf.calculate_cross_validation(classifier_type)

    classifier = clf.train_classifier(classifier_type)
    with open('classifier.pkl', 'wb') as pkl_file:
        pickle.dump((classifier), pkl_file, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Train a classifier.')
    parser.add_argument('class1', type=str, help='A path containing images for class 1.')
    parser.add_argument('class2', type=str, help='A path containing images for class 2.')
    parser.add_argument('classifier_type', type=str, help='Which classifier type to use.',
                        default='rf', choices=['svm', 'rf', 'logit'])

    args = parser.parse_args()

    cross_validate(args.class1, args.class2, args.classifier_type)
