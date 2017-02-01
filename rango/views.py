from datetime import datetime
from django.shortcuts import render, HttpResponse
from rango.models import Category, Page
from .forms import CategoryForm, PageForm


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    most_viewed_pages = Page.objects.order_by("-views")[:5]

    context_dict["pages"] = most_viewed_pages

    # Render the response and send it back!
    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, "rango/about.html", {"name": "Gabor"})


def show_category(request, category_name_slug):
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


def add_category(request):
    """
    Create a new category.
    """
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print form.errors
    return render(request, "rango/add_category.html", {"form": form})


def add_page(request, category_name_slug):
    """
    Create a new page.
    """
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print form.errors
    return render(request, "rango/add_page.html", {"form": form, "category": category})
