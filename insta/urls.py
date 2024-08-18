"""
Author: Farid Mohammadi
Date: 2024-08-15 09:53:18
LastEditors:
LastEditTime: 2024-08-15 09:53:18
FilePath: insta/urls.py
"""
from django.urls import path
from . import views


urlpatterns = [
    path("profile/<str:username>", views.profile, name="profile"),

]
