from django.contrib import admin
from Quizmanager.views import *
from django.urls import path

urlpatterns = [
    path('', startpage),
    path('startgame/', startgame),
    path('answercheck/', answercheck),
    path('lvl/<level>/<player>/<questionnum>/', gamepage),
    path('endgame/<player>/<level>/', endpage)
]
