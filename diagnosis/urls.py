from django.contrib import admin
from django.urls import path, include
from diagnosis import views

urlpatterns = [
    path("", views.home, name="home"),
    path("init", views.init, name="init"),
    path("track", views.choose_track, name="choose_track"),
    # path("complaint", views.init_evidence, name="init_evidence"),
    path("factors", views.risk_factors, name="risk_factors"),
    path("questions", views.questions, name="questions"),
    path("devs", views.devs, name="devs"),
    path("search", views.search, name="search"),
    path("complaint", views.complaint, name="complaint"),
    path("labresult", views.labresult, name="labresult"),
    path("diagnosis", views.diagnosis, name="diagnosis"),
]
