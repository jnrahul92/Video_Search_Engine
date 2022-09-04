# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 15:03:09 2022

@author: jnrah
"""
from django.urls import path

from .views import HomePageView, SearchResultsView

urlpatterns = [
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path("", HomePageView.as_view(), name="home"),
]
