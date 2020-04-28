#!python3
# -*- coding=UTF-8 -*-

# Create by Eric Li at 28.04.20 for FuzzyMiner

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def filter(request):
    return render(request, 'filter.html')

def help(request):
    return render(request, 'help.html')