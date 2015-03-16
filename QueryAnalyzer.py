'''
Created on 15.03.2015

@author: zissi
'''
from DataCleaner import DataCleaner
from RgbHistogramExtractor import RgbHistogramExtractor
from SiftFeatureExtractor import SiftFeatureExtractor

class QueryAnalyzer(object):
    '''
    Gets imagepath and trained classifier and returns predicted label of query.
    '''


    def __init__(self, image, classifier, vocabulary=None):
        self.image = image
        self.classifier = classifier
        self.vocabulary = vocabulary

    def _calculate_features(self):
        data_cleaner = DataCleaner('', cv=self.vocabulary is None)
        query = data_cleaner._resize_image(self.image)
        if self.vocabulary is None:
            hist_extactor = RgbHistogramExtractor([query])
            feature = hist_extactor.calc_hist()
        else:
            sift_extractor = SiftFeatureExtractor([query], vocabulary=self.vocabulary, quiet=True)
            feature = sift_extractor.extract_feature()
        return feature

    def predict_label(self):
        feature = self._calculate_features()
        result = self.classifier.predict(feature)
        return {0:"bird", 1:"penguin"}.get(result[0])
