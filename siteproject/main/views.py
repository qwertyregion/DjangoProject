from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, Http404


def home(request):
    return render(request, template_name='home.html')


def next1(request):
    fname = request.GET.get('fname')
    lname = request.GET.get('lname')
    dict_name = {'fname': fname,
                 "lname": lname,
                 }
    return render(request, template_name='next1.html', context=dict_name)


def next2(request, year=None):
    if year is None:
        year = 'год не определен '
        return render(request, template_name='next2.html', context={'year': year})
    if int(year) < 2000 or int(year) > 2023:
        return redirect('home', permanent=True)
    return render(request, template_name='next2.html', context={'year': year})


def pageNotFound(request, exception):
    return HttpResponseNotFound('ЭТА ССЫЛКА НЕДЕЙСТВИТЕЛЬНА', status=404)
