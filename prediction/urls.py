from django.urls import path
from .views import (
    PredictDiseaseView,
    PredictionHistoryView,
    SymptomsView
)

urlpatterns = [
    path('predict/', PredictDiseaseView.as_view()),
    path('history/', PredictionHistoryView.as_view()),
    path('symptoms/', SymptomsView.as_view()),
]