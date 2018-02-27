from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    context_dict = {'random':"random text"}
    return render(request, 'tvtrail/index.html', context=context_dict)


def about(request):
    context_dict = {'random':"random"}
    return render(request, 'tvtrail/about.html', context=context_dict)