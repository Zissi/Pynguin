'''
Created on 10.03.2015

@author: zissi
'''
import numpy as np
from sklearn import svm
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
class Classificator(object):
    '''
    classdocs
    '''

    def __init__(self, bird_features, penguin_features):
        self.bird_features = bird_features
        self.penguin_features = penguin_features
        
    def classify(self, classifier):
        features, labels = self._create_input()
        if classifier == "svm":
            clf = svm.SVC()
        elif classifier == "rf":
            clf = RandomForestClassifier(n_estimators=10, max_features=22)
        clf.fit(features, labels)
        return clf
           
    def _create_input(self):
        features = np.vstack([self.bird_features, self.penguin_features])
        labels = np.array(['bird'] * self.bird_features.shape[0] + ['penguin'] * self.penguin_features.shape[0])
        return features, labels

    def calculate_cross_validation(self, classifier):
        features, labels = self._create_input()
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(features, labels, test_size=0.40, random_state=0)
        if classifier == 'svm':
            clf = svm.SVC().fit(X_train, y_train)
        elif classifier == "rf":
            clf = RandomForestClassifier(n_estimators=10, max_features=22).fit(X_train, y_train)
        score = clf.score(X_test, y_test)
        print score
        return score
        
    
