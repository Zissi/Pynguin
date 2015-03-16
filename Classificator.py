'''
Created on 10.03.2015

@author: zissi
'''
import numpy as np
from sklearn import svm, cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.preprocessing.label import LabelEncoder

class Classificator(object):
    '''
    classdocs
    '''

    def __init__(self, penguin_features, bird_features):
        self.penguin_features = penguin_features
        self.bird_features = bird_features
        labels = np.array(["bird"] * self.bird_features.shape[0] + ["penguin"] * self.penguin_features.shape[0])
        self.label_encoder = LabelEncoder()
        self.labels = self.label_encoder.fit_transform(labels)

    def train_classifier(self, classifier):
        features, labels = self._create_input()
        if classifier == "svm":
            clf = svm.SVC()
        elif classifier == "rf":
            clf = RandomForestClassifier()
        elif classifier == "logit":
            clf = RandomForestClassifier()
        clf.fit(features, labels)
        return clf

    def _create_input(self):
        features = np.vstack([self.bird_features, self.penguin_features])
        return features, self.labels

    def calculate_cross_validation(self, classifier):
        features, labels = self._create_input()
        if classifier == 'svm':
            clf = svm.SVC()
        elif classifier == 'rf':
            clf = RandomForestClassifier()
        elif classifier == 'logit':
            clf = LogisticRegression()
        scores = cross_validation.cross_val_score(clf, features, labels, cv=5, scoring='precision')
        return scores.mean()

