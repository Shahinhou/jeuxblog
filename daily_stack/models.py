from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Assignment(models.Model):

    due_date = models.DateField(auto_now=False,auto_now_add=False)
    assigned_date = models.DateField(auto_now_add=True)
    difficulty = models.PositiveIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(5)])
    name = models.CharField(max_length=100, default="essay")

    def __str__(self):
        return self.name

class Stack(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    assignments = models.ManyToManyField(Assignment)

    def remove_assignment(self, a):
        self.assignments.remove(a)

