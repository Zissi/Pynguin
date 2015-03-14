'''
Created on 07.03.2015

@author: zissi
'''

from DataCleaner import DataCleaner
from OrbFeatureExtractor import OrbFeatureExtractor, QueryOrbFeatureExtractor
from Classificator import Classificator
import pickle
import os
from RgbHistogramExtractor import RgbHistogramExtractor


if __name__ == '__main__':
    pkl_path = 'pkl_file.bin'
    if os.path.exists(pkl_path):
        with open(pkl_path) as pkl_file:
            penguin_features, bird_features, vocabulary, bird_histogramms, penguin_histogramms = pickle.load(pkl_file)
            
    else:
        data_cleaner = DataCleaner('/media/Daten/Downloads/Flickr')
        clean_birds = data_cleaner.collect_and_resize()
    
        data_cleaner.images_folder = '/media/Daten/Downloads/penguin'
        clean_penguins = data_cleaner.collect_and_resize()
    
        orb = OrbFeatureExtractor(clean_penguins, clean_birds)
        penguin_features, bird_features = orb.extract_features()
        vocabulary = orb.vocabulary
        
        hist = RgbHistogramExtractor(clean_birds)
        bird_histogramms = hist.calc_hist()
        hist.images = clean_penguins
        penguin_histogramms = hist.calc_hist()
        
        with open(pkl_path, 'wb') as pkl_file:
            pickle.dump((penguin_features,
                         bird_features,
                         vocabulary, bird_histogramms, penguin_histogramms),
                        pkl_file, pickle.HIGHEST_PROTOCOL)
    
    clf = Classificator(penguin_histogramms, bird_histogramms)
    print clf.calculate_cross_validation('rf')
    
    classifier = clf.classify('rf')
    
    data_cleaner = DataCleaner('')
    query = data_cleaner._resize_image('/media/Daten/Downloads/Flickr/Barred Owl_14253146328_m.jpg')
    hist_extactor = RgbHistogramExtractor([query])
    query_hist = hist_extactor.calc_hist()
    result = classifier.predict(query_hist)
    print {0:"bird", 1:"penguin"}.get(result[0])
    
