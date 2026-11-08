from django.urls import path

from . import views

app_name = 'medications'

urlpatterns = [
    path('add/', views.medication_add, name='add'),
]
