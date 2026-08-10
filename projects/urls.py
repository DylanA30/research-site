from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.project_list, name="project_list"),
    path("news/<slug:slug>/", views.news_detail, name="news_detail"),
    path("<slug:slug>/", views.project_detail, name="project_detail"),
]