from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_exam, name='upload_exam'),
    path('exam/<uuid:pk>/', views.take_test, name='take_test'),
    path('dashboard/<uuid:pk>/', views.dashboard_view, name='dashboard_view'),
    path('dashboard/<uuid:pk>/download/', views.download_csv, name='download_csv'),
]