from django.urls import path

from . import views

app_name = 'games'

urlpatterns = [
    path('/', views.game_list, name='game_list'),
    path('/<str:title>/', views.game_detail, name='game_detail'),
]
