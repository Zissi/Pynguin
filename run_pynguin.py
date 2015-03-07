'''
Created on 07.03.2015

@author: zissi
'''

from DataCleaner import DataCleaner

if __name__ == '__main__':
    data_cleaner = DataCleaner('/media/Daten/Downloads/Flickr')
    clean_birds = data_cleaner.collect_and_resize()

    data_cleaner.images_folder = '/media/Daten/Downloads/penguin'
    clean_penguins = data_cleaner.collect_and_resize()
    print [x.shape for x in clean_penguins]
