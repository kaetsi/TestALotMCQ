from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_exam, name='upload_exam'),
    path('exam/<uuid:pk>/', views.take_test, name='take_test'),
]