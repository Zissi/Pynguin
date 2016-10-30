# Pynguin
Pynguin is a machine learning pipeline for image classification using different features like colour histograms and SIFT.
At the moment the classifier (`classifier.pkl`) is trained to differentiate penguins from other birds.

## Usage

### Training a classifier
To train your own classifier run the `train.py` script, passing two paths to folders containing images (of birds and penguins :wink:). The output will be the precision achieved using cross validation and a `classifier.pkl` file.

### Django web app
To run the django web app change your working directory to `pynguin_django` and run `python manage.py migrate` (you only need to do that once) and afterwards run `python manager.py runserver` whenever you want to start the server. To upload a file go to [127.0.0.1:8000/upload](127.0.0.1:8000/upload), select a file and click `submit`.

## Installation
As opencv and tkinter are both needed but hard to install in a virutalenv, it's best to install these two packages using your system's package manager (e.g. on Ubuntu `sudo apt-get install python-opencv python-tk`) and create a virtualenv that inherits from the global site package (using the `--system-site-package` flag). All other dependencies can be installed using the `requirements.txt`

## Copyright
All training images are taken from [photosforclass.com](http://www.photosforclass.com) and are distributed under Creative Commons.