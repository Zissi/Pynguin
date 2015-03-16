from QueryAnalyzer import QueryAnalyzer
import pickle
import sys

pkl_path = '/media/More_Storage/workspace/Pynguin/classifier.pkl'
with open(pkl_path) as pkl_file:
    classifier = pickle.load(pkl_file)

for test_image in sys.argv[1:]:
    print test_image
    query_analyzer = QueryAnalyzer(test_image, classifier)
    print query_analyzer.predict_label(), "(bird=ich; penguin=zissi)"
