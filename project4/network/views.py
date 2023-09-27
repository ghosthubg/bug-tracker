import re

from django.core.paginator import Paginator
from social_django.views import complete
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import requests
from django.contrib.auth.models import User
from .models import Bug, BugComment, Developer,AssignedDeveloper,ChangeStatus
from django import forms
from django.core.mail import send_mail
from django.db.models import Count
from .models import User


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        severity = request.POST.get('severity')
        screenshot = request.FILES.get('image')
        steps_to_reproduce = request.POST.get('steps_to_reproduce')
        reporter = request.POST.get('reporter')

        try:
            user_reporter = User.objects.get(username=reporter)
        except User.DoesNotExist:
            user_reporter = None

        if user_reporter:
            bug_form_items = Bug(
                title=title,
                description=description,
                status=status,
                severity=severity,
                screenshot=screenshot,
                steps_to_reproduce=steps_to_reproduce,
                reporter=user_reporter
            )
            bug_form_items.save()

            comment_texts = request.POST.getlist('comments')
            for comment_text in comment_texts:
                comment = BugComment(text=comment_text, commenter=user_reporter)
                comment.save()
                bug_form_items.comments.add(comment)

            return HttpResponseRedirect(reverse("index"))  # Add a debug message
        else:
            print("User not found:", reporter)  # Debug message for user not found

    return render(request, "network/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))






def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Validate email using regex
        if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email):
            return render(request, "network/register.html", {
                "message": "Invalid email format."
            })

        # Attempt to create a new user
        try:
            # Set the backend explicitly
            user = User(username=username, email=email, password=password)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username or email already taken."
            })

        # Log in the user
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# Handle the OAuth2 callback from Google
def google_oauth2_callback(request):
    response = complete(request, 'google-oauth2')

    # After successful OAuth2 authentication, redirect to the index page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    return response


#display all new bugs
from django.db import IntegrityError
from django.http import JsonResponse

# Your other imports

def bug_list(request):
    bugs = Bug.objects.all()  # Replace this with your query to fetch bugs
    paginator = Paginator(bugs, 2)  # Show 2 bugs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        bug_id = request.POST.get("bug_id")  # Get the bug ID from the form
        developer_email = request.POST.get("developer_email")
        developer_name = request.POST.get("developer_name")

        # Check if developer_email is not empty
        if developer_email:
            existing_developer = Developer.objects.filter(email=developer_email).first()

            if existing_developer:
                developer = existing_developer
            else:
                developer = Developer.objects.create(email=developer_email, name=developer_name)
            bug = Bug.objects.get(pk=bug_id)
            assign_dev = AssignedDeveloper(
                bug_id=bug_id,
                developer=developer,
            )

            try:
                assign_dev.save()
                # Send the email after successfully assigning the developer
                subject = f'Bug Assignment: {bug_id}'
                message = f'You have been assigned to handle Bug ID {bug_id},' \
                          f' Description of bug: {bug.description}.'
                from_email = 'syloncube837@gmail.com'
                recipient_list = [developer_email]

                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                return JsonResponse({'message': 'Developer assigned successfully'})
            except IntegrityError as e:
                # Handle the IntegrityError as needed
                print("IntegrityError:", e)
                return JsonResponse({'message': 'Error assigning developer'})
        else:
            # Handle the case where developer_email is empty
            print("Developer email is empty")
            return JsonResponse({'message': 'Developer email is empty'})

    if request.method == "POST":
        # ... Your POST handling code ...
        status_choices = Bug.STATUS_CHOICES
    else:
        # Get the STATUS_CHOICES from the Bug model
        status_choices = Bug.STATUS_CHOICES

    return render(request, 'network/bug_list.html', {
        "bug": page_obj,
        "developer": Developer.objects.all(),
        "status":ChangeStatus.objects.all(),
        "status_choices": status_choices,
    })
def update_bug_status(request):
    if request.method == 'POST':
        bug_id = request.POST.get('bug_id')
        status = request.POST.get('status')
        try:
            bug = Bug.objects.get(pk=bug_id)
            bug.status = status
            bug.save()
            return JsonResponse({'message': 'Status updated successfully'})
        except Bug.DoesNotExist:
            return JsonResponse({'message': 'Bug not found'}, status=404)

def save_change_status(request):
    if request.method == 'POST':
        bug_id = request.POST.get('bug_id')
        status = request.POST.get('status')
        # Create a new ChangeStatus entry
        ChangeStatus.objects.create(bug_id=bug_id, status=status)
        return JsonResponse({'message': 'Status change saved in ChangeStatus model'})

#developers function
def developers(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']

        developers= Developer(
            name=name,
            email=email
        )
        developers.save()

    return render(request,"network/developers.html")

def changestatus(request):
    if request.method == 'POST':
        bug_id = request.POST.get('bug_id')
        new_status = request.POST.get('status')

        bug = get_object_or_404(Bug, pk=bug_id)
        bug.status = new_status
        bug.save()

        return JsonResponse({'message': 'Status updated successfully'})

    return JsonResponse({'message': 'Invalid request method'})


def dashboard(request):
    # Define the severity levels you want to filter by
    severity_levels = ['low', 'medium', 'high']

    # Initialize empty lists for labels and data
    labels = []
    data = []

    # Loop through the severity levels
    for severity_level in severity_levels:
        count = Bug.objects.filter(severity=severity_level).count()
        labels.append(severity_level)
        data.append(count)

    status_levels = ['new', 'fixed','under_review']
    # Initialize empty lists for labels and data
    labelset = []
    dataset = []

    # Loop through the severity levels
    for status_level in status_levels:
        count = Bug.objects.filter(status=status_level).count()
        labelset.append(status_level)
        dataset.append(count)

    assign_dev= ['1']
    # Initialize empty lists for labels and data
    labelset1 = []
    dataset1 = []

    # Loop through the devs levels
    for assign_devs in assign_dev:
        count = AssignedDeveloper.objects.filter(developer=assign_devs).count()
        labelset1.append(assign_devs)
        dataset1.append(count)

    return render(request, "network/dashboard.html", {
        'labels': labels,
        'data': data,
        'labelset':labelset,
        'dataset':dataset,
        'labelset1':labelset1,
        'dataset1':dataset1

    })


