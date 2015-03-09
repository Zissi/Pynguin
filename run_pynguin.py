'''
Created on 07.03.2015

@author: zissi
'''

from DataCleaner import DataCleaner
from OrbFeatureExtractor import OrbFeatureExtractor

if __name__ == '__main__':
    data_cleaner = DataCleaner('/media/Daten/Downloads/Flickr')
    clean_birds = data_cleaner.collect_and_resize()

    data_cleaner.images_folder = '/media/Daten/Downloads/penguin'
    clean_penguins = data_cleaner.collect_and_resize()

    orb = OrbFeatureExtractor(clean_penguins[:5])
    penguin_features = orb.extract_features()
    
    orb.images = clean_birds[:5]
    bird_features = orb.extract_features()
    print bird_features
    
