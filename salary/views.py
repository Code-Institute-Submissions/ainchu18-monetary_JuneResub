from django.shortcuts import render, redirect
from .models import Source, Salary
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
import datetime
import csv


def index(request):
    sources = Source.objects.all()
    salary = Salary.objects.filter(owner=request.user)
    paginator = Paginator(salary, 5)
    page_num = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_num)

    context = {
        'salary': salary,
        'page_obj': page_obj
    }
    return render(request, 'salary/index.html', context)


def add_salary(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'salary/add_salary.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'salary/add_salary.html', context)
        description = request.POST['description']
        date = request.POST['salary_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'salary/add_salary.html', context)

        if not date:
            messages.error(request, 'Salary date is required')
            return render(request, 'salary/add_salary.html', context)

        if not source:
            messages.error(request, 'Source is required')
            return render(request, 'salary/add_salary.html', context)

        Salary.objects.create(owner=request.user, amount=amount,
                               date=date, source=source, description=description)
        messages.success(request, 'Salary saved successfully')
        return redirect('salary')
