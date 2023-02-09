from django.shortcuts import render
from .apps import PredictorConfig
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from .forms import UserForm, ResultForm

import re
from stop_words import get_stop_words

# Create your views here.

def full_preprocess(text):
    
    stop_words = list(get_stop_words('en')) 
    tags = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    punkt = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\#)|(\*)|(\n)")
    text_1 = str(text)
    new_text = text_1.split(' ')
    output = [w.lower() for w in new_text if not w in stop_words]
    last_out = (" ").join(output)
    without_tags = re.sub(tags, r' ', last_out)
    without_punkt = re.sub(punkt, r'', without_tags)
    without_one_letter = re.sub('(\\b[A-Za-z] \\b|\\b [A-Zaa-z]\\b)', r' ', without_punkt).strip()
    return without_one_letter

def gett(request):
    if request.method == 'GET':
        text = request.GET.get('result')
        if text !='':
            new_text = full_preprocess(text)
            vector = PredictorConfig.tfidf.transform([new_text])
            prediction_class = PredictorConfig.sgd_class.predict(vector)
            prediction_rating = PredictorConfig.sgd_rating.predict(vector)
            if prediction_class == 'neg':
                screen_pred = f'негативный'
            else:
                screen_pred = f'позитивный'
            response = {'header': screen_pred, 'rating': int(prediction_rating)}

        else :
            screen_pred = 'Вы не ввели комментарий!!!'
            prediction_rating = 'Комментария нет, рейтинг не определен'
            response = {'header': screen_pred, 'rating': prediction_rating}

    userform = UserForm()
    return render(request, 'index.html', context=response)
