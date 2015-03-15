from django import forms
from django.shortcuts import render
import os
from tempfile import NamedTemporaryFile
from QueryAnalyizer import QueryAnalyzer
import pickle
from pynguin_django import settings
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError

pkl_path = '/home/derdot/workspace/Pynguin/classifier.pkl'
with open(pkl_path) as pkl_file:
    classifier = pickle.load(pkl_file)

class RestrictedFileField(forms.FileField):

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")

        forms.FileField.__init__(self, *args, **kwargs)

    def clean(self, data, initial=None):
        afile = forms.FileField.clean(self, data, initial)

        try:
            content_type = afile.content_type.split("/")[0]
            if content_type in self.content_types:
                if afile._size > self.max_upload_size:
                    raise ValidationError('Please keep filesize under %s. Current filesize %s' % (filesizeformat(self.max_upload_size), filesizeformat(afile._size)))
            else:
                raise ValidationError('Filetype not supported.')
        except AttributeError:
            pass

        return data

class UploadFileForm(forms.Form):
    image = RestrictedFileField(content_types=settings.CONTENT_TYPES,
                                max_upload_size=settings.MAX_UPLOAD_SIZE)
    
def upload_file(request):
    image_name = None
    classification = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            image_name = save_image(request)
            classification = analyze_query(image_name)
            image_name = os.path.basename(image_name)
    else:
        form = UploadFileForm()
    return render(request, 'img_classifier/index.html', {'form':form,
                                                         "image":image_name,
                                                         'classification':classification})
 
def save_image(request):
    filename = get_filename(request)
    with open(filename, 'wb+') as destination:
        for chunk in request.FILES['image'].chunks():
            destination.write(chunk)
    return filename

def get_filename(request):
    original_name = request.FILES['image'].name
    extension = os.path.splitext(original_name)[1]
    tmpf = NamedTemporaryFile(delete=False, suffix=extension, dir='img_classifier/images')
    new_name = tmpf.name
    tmpf.close()
    return new_name

def analyze_query(image_name):
    query_analyzer = QueryAnalyzer(image_name, classifier)
    return query_analyzer.predict_label()
    