'''
Created on 10.03.2015

@author: zissi
'''
import numpy as np
from sklearn import svm
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets
from sklearn.linear_model.logistic import LogisticRegression
class Classificator(object):
    '''
    classdocs
    '''

    def __init__(self, penguin_features, bird_features):
        self.penguin_features = penguin_features
        self.bird_features = bird_features
        
    def classify(self, classifier):
        features, labels = self._create_input()  
        if classifier == "svm":
            clf = svm.SVC()
        elif classifier == "rf":
            clf = RandomForestClassifier(n_estimators=10, max_features=22)
        clf.fit(features, labels)
        return clf
           
    def _create_input(self):
        labels = np.array([0] * self.bird_features.shape[0] + [1] * self.penguin_features.shape[0])
        features = np.vstack((self.bird_features, self.penguin_features))
        return features, labels

    def calculate_cross_validation(self, classifier):
        features, labels = self._create_input()
        if classifier == 'svm':
            clf = svm.SVC()
        elif classifier == 'rf':
            clf = RandomForestClassifier(n_estimators=10)
        elif classifier == 'logit':
            clf = LogisticRegression()
        scores = cross_validation.cross_val_score(clf, features, labels, cv=10, scoring='precision')
        return scores.mean()      
    
