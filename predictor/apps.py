from django.apps import AppConfig
from django.conf import settings

import os
import joblib


class PredictorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "predictor"

    path = os.path.join(settings.MODELS)
    
    tfidf = joblib.load(path + 'TFIDF.pkl')
    sgd_class = joblib.load(path + 'SGD_class.pkl')
    sgd_rating = joblib.load(path + 'SGD_rating.pkl')
