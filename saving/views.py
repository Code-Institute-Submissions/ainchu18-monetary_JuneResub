from django.shortcuts import render, redirect
from .models import Source, Saving
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
import datetime
import csv


@login_required(login_url='/accounts/login')
def index(request):
    sources = Source.objects.all()
    saving = Saving.objects.filter(owner=request.user)
    paginator = Paginator(saving, 5)
    page_num = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_num)

    context = {
        'saving': saving,
        'page_obj': page_obj
    }
    return render(request, 'saving/index.html', context)