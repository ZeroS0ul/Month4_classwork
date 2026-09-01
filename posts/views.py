from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def hello_world(r):
    return HttpResponse("/<h1>Hello World!</h1>")

def my_name(r):
    name = "John "
    return HttpResponse(f"<h2>hello </h2> <h1> {name}</h1>")


def say_name(r, name):
    return HttpResponse(f"<h2>hello </h2> <h1> {name}</h1>")


