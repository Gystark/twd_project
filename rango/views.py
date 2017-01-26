from django.shortcuts import render, HttpResponse
from rango.models import Category, Page


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    most_viewed_pages = Page.objects.order_by("-views")[:3]

    context_dict["most_viewed_pages"] = most_viewed_pages

    # Render the response and send it back!
    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, "rango/about.html", {"name": "Gabor"})


def view_category(request, category_name_slug):
    context = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context["category"] = category
        context["pages"] = pages
    except Category.DoesNotExist:
        context["category"] = None
        context["pages"] = None

    return render(request, "rango/category.html", context)