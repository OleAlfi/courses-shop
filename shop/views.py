from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Course, Review
from django.contrib.auth import login
from .forms import PaymentForm, RegisterForm, ReviewForm
from django.contrib import messages


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "shop/courses.html"
    context_object_name = "courses"
    paginate_by = 3

    def get_queryset(self):
        queryset = Course.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "shop/single_course.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_already_reviewed = False
        if self.request.user.is_authenticated:
            user_already_reviewed = Review.objects.filter(
                course=self.object,
                user=self.request.user
            ).exists()

        context['user_already_reviewed'] = user_already_reviewed
        context['review_form'] = ReviewForm()
        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.course = self.object
            review.user = request.user
            review.save()
            return redirect("shop:single_course", pk=self.object.pk)

        context = self.get_context_data()
        context["review_form"] = form
        return self.render_to_response(context)


def signup(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "registration/login.html", {"form": form})

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("shop:index")
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def payment(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            messages.success(request, f"Payment for {course.title} successful! Enjoy your learning.")
            return redirect("shop:index")
    else:
        form = PaymentForm(initial={"amount": course.price})
    return render(request, "shop/payment.html", {"course": course, "form": form})