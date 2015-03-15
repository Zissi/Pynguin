'''
Created on 07.03.2015

@author: zissi
'''

from DataCleaner import DataCleaner
from OrbFeatureExtractor import OrbFeatureExtractor
from Classificator import Classificator
import pickle
import os
from RgbHistogramExtractor import RgbHistogramExtractor
from QueryAnalyizer import QueryAnalyzer


if __name__ == '__main__':
    pkl_path = 'histograms.pkl'
    if os.path.exists(pkl_path):
        with open(pkl_path) as pkl_file:
            bird_histogramms, penguin_histogramms = pickle.load(pkl_file)
            
    else:
        data_cleaner = DataCleaner('/media/Daten/Downloads/Flickr')
        clean_birds = data_cleaner.collect_and_resize()
    
        data_cleaner.images_folder = '/media/Daten/Downloads/penguin'
        clean_penguins = data_cleaner.collect_and_resize()
        
        hist = RgbHistogramExtractor(clean_birds)
        bird_histogramms = hist.calc_hist()
        hist.images = clean_penguins
        penguin_histogramms = hist.calc_hist()
        
        with open(pkl_path, 'wb') as pkl_file:
            pickle.dump((bird_histogramms, penguin_histogramms),
                        pkl_file, pickle.HIGHEST_PROTOCOL)
            
    
    clf = Classificator(penguin_histogramms, bird_histogramms)
    print clf.calculate_cross_validation('rf')
    
    classifier = clf.train_classifier('rf')
    with open('classifier.pkl', 'wb') as pkl_file:
            pickle.dump((classifier),
                        pkl_file, pickle.HIGHEST_PROTOCOL)

