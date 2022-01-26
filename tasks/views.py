# Add your Views Here
# Add all your views here
from asyncio import tasks
from multiprocessing import context
from turtle import title

from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import path

from tasks.models import Task


completed_task = []

def tasks_filter(task):
    if(task in completed_task):
        return True
    else:
        return False

if len(completed_task) > 0:
    tasks = filter(tasks_filter , tasks)
    

def tasks_view(request):
    search_item = request.GET.get("search")    
    tasks = Task.objects.filter(deleted=False).filter(completed=False)
    if search_item:
        tasks = tasks.filter(title__icontains=search_item)
    return render(request , "tasks.html" , {"tasks" : tasks})



def add_task_view(req):
    task_value = req.GET.get("task")
    Task(title=task_value).save()
    #tasks.append(task_value)
                  
    return HttpResponseRedirect("/tasks")

def delete_task_view(req , index):
    Task.objects.filter(id=index).update(deleted=True)
    return HttpResponseRedirect("/tasks")


def complete_task_view(req , index):
    Task.objects.filter(id=index).update(completed=True)
    return HttpResponseRedirect("/tasks")


def completed_task_view(req):
    context = {
        
    }
    return render(req , "completed.html" , {"tasks" : Task.objects.filter(completed=True).filter(deleted=False)})


def all_tasks_view(req):
    context = {
        "ptasks" : Task.objects.filter(deleted=False).filter(completed=False),
        "ctasks" : Task.objects.filter(deleted=False).filter(completed=True)
    }
    return render(req , 'index.html' , context)
