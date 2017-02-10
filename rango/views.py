from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.urls import reverse

from rango.models import Category, Page
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm


def get_server_side_cookie(request, cookie, default_val=None):
    """
    Get the value of a server-side cookie
    """
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    """
    Handle the visitor cookies.
    """
    # Get the number of visits from the session cookie
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()) )

    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).seconds > 0:
        visits += 1
        # update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # update/set the visits cookie
    request.session['visits'] = visits


def index(request):
    """
    View the 5 most liked categories and the 5 most viewed pages.
    """
    request.session.set_test_cookie()

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    most_viewed_pages = Page.objects.order_by("-views")[:5]

    context_dict["pages"] = most_viewed_pages

    # Call function to handle the cookies
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    return render(request, 'rango/index.html', context_dict)


def about(request):
    """
    About page view, which displays the author name, the number of visits
    and a cute cat picture.
    """
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()

    context = {}
    context['name'] = "rango"

    # Call function to handle the cookies
    visitor_cookie_handler(request)
    context['visits'] = request.session['visits']

    return render(request, "rango/about.html", context)


def show_category(request, category_name_slug):
    """
    Show a category based on its slug if it exists,
    along with all pages in that category.
    """
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


@login_required
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


@login_required
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


def register(request):
    """
    Simple registration view.
    """
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Get data from both forms
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Hash and save the password
            user.set_password(user.password)
            user.save()

            # Save the user profile and link it to the user
            profile = profile_form.save(commit=False)
            profile.user = user

            # If there is an uploaded avatr, set it as the user's profile picture
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            # Print the form errors
            print(user_form.errors, profile_form.errors)
    else:
        # Not HTTP POST, so display the forms
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    """
    Hanlde loging users in.
    """
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Get the username and password
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate using Django's built-in method
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # Call Django's login method and return to the index view
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    # Only HTTP POST requests are dealt with, others just render the login page
    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    """
    A view only visible to logged in users.
    """
    return render(request, "rango/restricted.html", {})


@login_required
def user_logout(request):
    """
    Handle logging users out using the built-in logout method
    """
    logout(request)
    # Return to the index page
    return HttpResponseRedirect(reverse('index'))
