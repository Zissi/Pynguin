'''
Created on 10.03.2015

@author: zissi
'''
import cv2
import numpy as np

class RgbHistogramExtractor(object):
    '''
    classdocs
    '''


    def __init__(self, images):
        self.images = images
        
 #   def calc_np_hist(self):
 #       histogramms = np.ndarray((len(self.images), 512))
 #       for image in self.images:
#            print image.shape
#            hist = np.histogramdd(image, 8, [0, 256], normed=True)
 #           print hist[0].shape
  #           np.vstack([histogramms, hist[0]])  # hist[1] are the bins which are equally spaced
   #     return histogramms
        
        
    def calc_hist(self):
        histogramms = []
        for image in self.images:
            hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist = hist.astype(np.int32).flatten()
            histogramms.append(hist)
        histogramms = np.vstack(histogramms)
        return histogramms


