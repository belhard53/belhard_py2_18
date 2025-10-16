from django.shortcuts import render
from django.http import HttpResponse
from .models import Student

# Create your views here.



def index(r):
    return render(r, 'base.html')


def students(r):
    students = Student.objects.all()
    return render(r, 'students.html', 
                    context={'students':students})