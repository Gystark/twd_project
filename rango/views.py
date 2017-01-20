from django.shortcuts import render, HttpResponse


def index(request):

    context = {"name": "This is the name."}
    context["value"] = "This is the value."

    return render(request, "rango/index.html", context)


def about(request):
    return render(request, "rango/about.html", {"name": "Gabor"})