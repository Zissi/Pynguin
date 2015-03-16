from QueryAnalyzer import QueryAnalyzer
import pickle
import sys
import os

pkl_path = '/media/More_Storage/workspace/Pynguin/classifier_hist.pkl'
with open(pkl_path) as pkl_file:
    classifier_hist = pickle.load(pkl_file)

print "HISTOGRAMS"
print sys.argv[1]
for afile in os.listdir(sys.argv[1]):
    test_image = os.path.join(sys.argv[1], afile)
    query_analyzer = QueryAnalyzer(test_image, classifier_hist)
    print query_analyzer.predict_label(), "(bird=leaves; penguin=bikes)"
print
print sys.argv[2]
for afile in os.listdir(sys.argv[2]):
    test_image = os.path.join(sys.argv[2], afile)
    query_analyzer = QueryAnalyzer(test_image, classifier_hist)
    print query_analyzer.predict_label(), "(bird=leaves; penguin=bikes)"

pkl_path = '/media/More_Storage/workspace/Pynguin/classifier_sift.pkl'
with open(pkl_path) as pkl_file:
    classifier_sift = pickle.load(pkl_file)

pkl_path = '/media/More_Storage/workspace/Pynguin/viswords.pkl'
with open(pkl_path) as pkl_file:
    _, _, vocabulary = pickle.load(pkl_file)
print
print "SIFT"
print sys.argv[1]
for afile in os.listdir(sys.argv[1]):
    test_image = os.path.join(sys.argv[1], afile)
    query_analyzer = QueryAnalyzer(test_image, classifier_sift, vocabulary)
    print query_analyzer.predict_label(), "(bird=leaves; penguin=bikes)"
print
print sys.argv[2]
for afile in os.listdir(sys.argv[2]):
    test_image = os.path.join(sys.argv[2], afile)
    query_analyzer = QueryAnalyzer(test_image, classifier_sift, vocabulary)
    print query_analyzer.predict_label(), "(bird=leaves; penguin=bikes)"
