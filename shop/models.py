from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone
from django.conf import settings

class Category(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(default="", blank=True)
    price = models.FloatField()
    students_quantity =  models.IntegerField()
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    short_description = models.TextField(default="", blank=True)

    def __str__(self):
        return self.title

    def get_average_rating(self):
        average = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(average, 1) if average else 0

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate from 1 to 5"
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("course", "user")

    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.rating})"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("course", "user")

    def __str__(self):
        return f"{self.user.username} bought {self.course.title}"

