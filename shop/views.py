from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Course
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@login_required
def index(request):
    courses = Course.objects.all()
    return render(request, "shop/courses.html", {"courses": courses})

@login_required
def single_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "shop/single_course.html", {"course": course})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("shop:index")
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})