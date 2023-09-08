from django.urls import include,path
from . import views

app_name = "daily_stack"

urlpatterns = [

        path("", views.index, name="index"),
        path("<int:assignment_id>", views.assignment, name="assignment"),

        ]
