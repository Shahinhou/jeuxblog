from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your views here.

class assignmentForm(forms.Form):
    name = forms.CharField(label="Assignment name")
    due_date = forms.DateField(label="Due date")
    difficulty = forms.IntegerField(label="Difficulty (1-5)", validators=[MinValueValidator(1), MaxValueValidator(5)])

#class removeForm(forms.Form):

def index(request):
    
    try:
        stack = Stack.objects.get(user=request.user.id)

    except Stack.DoesNotExist:
        print('stackless')

        stack = Stack(user=request.user.id)
        assignments = stack.assignments.all()
        return render(request, "daily_stack/index.html", {
            "stack":assignments,
            "form":assignmentForm(),
                })


    assignments = (stack.assignments.all())
    if request.method=="POST" and "remove_btn" not in request.POST:

        form = assignmentForm(request.POST)
        

        if form.is_valid():
            name = request.POST.get('name')
            due_date = request.POST.get('due_date')
            difficulty = request.POST.get('difficulty')

            a = Assignment(name=name,due_date=due_date,difficulty=difficulty)
            a.save()

         
            # don't repeat code. re-structure later.

            stack.assignments.add(a)
            stack.save()

            assignments = stack.assignments.all()
            
            return render(request, "daily_stack/index.html", {
                "form": assignmentForm(),
                "stack":assignments,
                })
        
        elif request.method=="POST" and "remove_btn" in request.POST:
            pass
            # do something

        else:
            return render(request, "daily_stack/index.html", {
                "form": assignmentForm(),
                "stack":assignments,
                })

    return render(request, "daily_stack/index.html", {
        "form": assignmentForm(),
        "stack":assignments,
        })

def assignment(request, assignment_id):
    
    assignment = Assignment.objects.get(pk=assignment_id)
    stack = Stack.objects.get(user=request.user.id)

    if request.method=="POST":
        print("posting")
        stack.remove_assignment(assignment)
        return redirect("daily_stack:index")

    
    return render(request, "daily_stack/assignment.html",{
        "assignment":assignment,
        })


