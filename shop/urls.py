from django.urls import path
from . import views

app_name = "shop"
urlpatterns = [
    path("", views.CourseListView.as_view(), name="index"),
    path("<int:pk>/", views.CourseDetailView.as_view(), name="single_course"),
    path("signup/", views.signup, name="signup"),
    path("<int:course_id>/payment/", views.payment, name="payment"),
    path("my-courses/", views.OrderListView.as_view(), name="my_courses"),

]