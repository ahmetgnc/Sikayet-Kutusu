from django.shortcuts import render
from .forms import PostForm
from django.shortcuts import redirect
import os
import pickle
from nltk.tokenize import RegexpTokenizer
import re

# Create your views here.
def post_list(request):
    return render(request, 'blog/post_list.html', {})

def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_list.html', {'form': form})


def succesView(request):
    compliant_text= 'Null'
    if request.method == "POST":
        compliant_text = request.POST.get('compliant_text')
        compliant_category = make_prediction(compliant_text)
        # compliant_category = str(os.getcwd())
    return render(request, 'blog/success.html', {'result_text': compliant_category})


def predict_category(result):
    if result[0] == 0:
        result = 'Eğitim'
    elif result[0] == 1:
        result = 'Elektronik'
    elif result[0] == 2:
        result = 'Gıda'
    elif result[0] == 3:
        result = 'Sağlık'
    else : result = 'Tespit Edilemedi'
    return result

def make_prediction(text):
    filename = os.getcwd() + '/blog/model/' + 'model.sav'
    model = pickle.load(open(filename, 'rb'))
    tokenizer = RegexpTokenizer(r'\w+')
    num_filter = re.sub(r'\d+', '', text)
    tokens = tokenizer.tokenize(num_filter)
    result = model.predict(tokens)
    compliant_category = predict_category(result)
    return compliant_category