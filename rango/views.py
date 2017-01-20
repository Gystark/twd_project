from django.shortcuts import render, HttpResponse
from rango.models import Category


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # Render the response and send it back!
    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, "rango/about.html", {"name": "Gabor"})