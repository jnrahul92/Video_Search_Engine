from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView
from django.db.models import Q

import pickle
from .models import video

index_file =  r"D:\M Tech DSE Bits\Semester 3\Information Retrieval\Assignments\Assignment 2\video_search\index.pkl"


class HomePageView(TemplateView):
    template_name = 'home.html'

class SearchResultsView(ListView):
    model = video
    template_name = 'search_results.html'
    def queryset(self):
        query = self.request.GET.get("q")
        with open(index_file, "rb") as f:
            index_dict = pickle.load(f)
        query_result1 = index_dict.get(query,"")
        query_result2 = index_dict.get(query.lower(),"")
        query_result = list(set(query_result1 + query_result2))
        i = 1
        for q in query_result:
            if i == 1:
                qs = video.objects.filter(Q(name__icontains = q[:-4]))
                i += 1
            else:
                temp = video.objects.filter(Q(name__icontains = q[:-4]))
                qs = qs.union(temp)
        try:
            return qs
        except:
            return video.objects.none()