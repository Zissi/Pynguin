'''
Created on 15.03.2015

@author: zissi
'''
from DataCleaner import DataCleaner
from RgbHistogramExtractor import RgbHistogramExtractor

class QueryAnalyzer(object):
    '''
    Gets imagepath and trained classifier and returns predicted label of query.
    '''


    def __init__(self, image, classifier):
        self.image = image
        self.classifier = classifier
        
    def _calculate_features(self):
        data_cleaner = DataCleaner('')
        query = data_cleaner._resize_image(self.image)
        hist_extactor = RgbHistogramExtractor([query])
        query_hist = hist_extactor.calc_hist()
        return query_hist
    
    def predict_label(self):
        query_hist = self._calculate_features()
        result = self.classifier.predict(query_hist)
        return {0:"bird", 1:"penguin"}.get(result[0])
        