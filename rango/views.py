from django.shortcuts import render, HttpResponse


def index(request):
    return render(request, "rango/index.html", {})


def about(request):
    return HttpResponse("about page")