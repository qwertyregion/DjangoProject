from django.shortcuts import render


def home(request):
    return render(request, template_name='home.html')


def next1(request):
    fname = request.GET.get('fname')
    lname = request.GET.get('lname')
    dict_name = {'fname': fname,
                 "lname": lname,
                 }
    return render(request, template_name='next1.html', context=dict_name)


