# api/urls.py
from django.urls import path
from .views import FaceDetectView

urlpatterns = [
    path('detect/', FaceDetectView.as_view()),
]
