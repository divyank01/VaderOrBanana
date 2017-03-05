from scipy.misc import imread
from django.shortcuts import render
from .forms import UploadForm
from .models import Upload
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


import base64

import pandas as pd
from sklearn.datasets import load_digits
import scipy
from os import listdir
from sklearn.decomposition import RandomizedPCA
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.manifold import Isomap
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from skimage.transform import resize
# Create your views here.
def SignIn(request):
    answer=None
    img = None
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Upload(data = request.FILES['docfile'])
            img=base64.b64encode(newdoc.data.read())
            try:
                answer=get_prediction(scipy.misc.imresize(imread(newdoc.data),(80,80)).flatten())
            except Exception:
            	return render_to_response(
                'error.html',
                {},
            )
    else:
        form = UploadForm() 
    return render_to_response(
        'home.html',
        {'form': form,'predict':answer,'image':img},
    )

clf = KNeighborsClassifier(n_jobs=2000)

def load_imgs():
	path1='/home/divyank/divyank/ml/data/dv/'
	path2='/home/divyank/divyank/ml/data/banana/'
	imgs=list()
	labels=list()
	for f in listdir(path1):
		labels.append('1')
		imgs.append(scipy.misc.imread(path1+f).flatten())
	for f in listdir(path2):
		labels.append('2')
		imgs.append(scipy.misc.imread(path2+f).flatten())
	return (np.array(labels),np.array(imgs))

def setup(request):
	df=load_imgs()
	train_data, test_data, train_label, test_label = train_test_split(df[1], df[0], random_state=200)
	clf.fit(train_data, train_label)
	form = UploadForm()
	return render_to_response(
        'home.html',
        {'form': form},
    )

def get_prediction(test_data):
	predicted = clf.predict(test_data)
	ids = {'1': 'Darth vader', '2': 'banana'}
	print(ids[predicted[0]])
	return ids[predicted[0]]
