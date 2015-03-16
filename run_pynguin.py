'''
Created on 07.03.2015

@author: zissi
'''

from DataCleaner import DataCleaner
from Classificator import Classificator
import pickle
import os
from RgbHistogramExtractor import RgbHistogramExtractor
from SiftFeatureExtractor import SiftFeatureExtractor


if __name__ == '__main__':
    import sys
    pkl_path_hist = 'histograms.pkl'
    if os.path.exists(pkl_path_hist):
        with open(pkl_path_hist) as pkl_file:
            bird_histogramms, penguin_histogramms = pickle.load(pkl_file)

    else:
        data_cleaner = DataCleaner(sys.argv[1])
        clean_birds = data_cleaner.collect_and_resize()

        data_cleaner.images_folder = sys.argv[2]
        clean_penguins = data_cleaner.collect_and_resize()

        hist = RgbHistogramExtractor(clean_birds)
        bird_histogramms = hist.calc_hist()
        hist.images = clean_penguins
        penguin_histogramms = hist.calc_hist()

        with open(pkl_path_hist, 'wb') as pkl_file:
            pickle.dump((bird_histogramms, penguin_histogramms),
                        pkl_file, pickle.HIGHEST_PROTOCOL)

    clf = Classificator(penguin_histogramms, bird_histogramms)
    print clf.calculate_cross_validation('rf')

    classifier = clf.train_classifier('rf')
    with open('classifier_hist.pkl', 'wb') as pkl_file:
            pickle.dump((classifier),
                        pkl_file, pickle.HIGHEST_PROTOCOL)

    pkl_path_viswords = 'viswords.pkl'
    if os.path.exists(pkl_path_viswords):
        with open(pkl_path_viswords) as pkl_file:
            bird_features, penguine_features, vocabulary = pickle.load(pkl_file)

    else:
        data_cleaner = DataCleaner(sys.argv[1], cv=False)
        clean_birds = data_cleaner.collect_and_resize()

        data_cleaner.images_folder = sys.argv[2]
        clean_penguins = data_cleaner.collect_and_resize()
        sift = SiftFeatureExtractor(clean_penguins, clean_birds)
        penguine_features, bird_features, vocabulary = sift.extract_features()

        with open(pkl_path_viswords, 'wb') as pkl_file:
            pickle.dump((bird_features, penguine_features, vocabulary),
                        pkl_file, pickle.HIGHEST_PROTOCOL)

    clf = Classificator(penguine_features, bird_features)
    print clf.calculate_cross_validation('svm')

    classifier = clf.train_classifier('svm')
    with open('classifier_sift.pkl', 'wb') as pkl_file:
            pickle.dump((classifier),
                        pkl_file, pickle.HIGHEST_PROTOCOL)