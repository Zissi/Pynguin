'''
Created on 07.03.2015

@author: zissi
'''

from DataCleaner import DataCleaner
from OrbFeatureExtractor import OrbFeatureExtractor
from Classificator import Classificator
from RgbHistogramExtractor import RgbHistogramExtractor

if __name__ == '__main__':
    data_cleaner = DataCleaner('/media/Daten/Downloads/Flickr')
    clean_birds = data_cleaner.collect_and_resize()

    data_cleaner.images_folder = '/media/Daten/Downloads/penguin'
    clean_penguins = data_cleaner.collect_and_resize()
    
    hist = RgbHistogramExtractor(clean_birds)
    bird_histogramms = hist.calc_hist()
    
    hist.images = clean_penguins
    penguin_histogramms = hist.calc_hist()




    orb = OrbFeatureExtractor(clean_penguins)
    penguin_features = orb.extract_features()
     
    orb.images = clean_birds
    bird_features = orb.extract_features()

    clf = Classificator(bird_histogramms, penguin_histogramms)
    svm_clf = clf.classify('svm')
