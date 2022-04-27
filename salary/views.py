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


@login_required(login_url='/accounts/login')
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


@login_required(login_url='/accounts/login')
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


@login_required(login_url='/accounts/login')
def salary_edit(request, id):
    sources = Source.objects.all()
    salary = Salary.objects.get(pk=id)
    context = {
        'salary': salary,
        'values': salary,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'salary/edit-salary.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'salary/edit-salary.html', context)
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

        salary.amount = amount
        salary.date = date
        salary.source = source
        salary.description = description

        salary.save()

        messages.success(request, 'Salary updated successfully')
        return redirect('salary')

        messages.info(request, 'Editing salary, please wait')
        return render(request, 'salary/edit-salary.html', context)


@login_required(login_url='/accounts/login')
def delete_salary(request, id):
    salary = Salary.objects.get(pk=id)
    if request.method == 'POST':
        salary.delete()
        messages.success(request, 'Salary deleted successfully')
        return redirect('salary')
    return render(request, 'salary/delete-salary.html')


def search_salary(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        salaries = Salary.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Salary.objects.filter(
            date__istartswith=search_str, owner=request.user) | Salary.objects.filter(
            description__icontains=search_str, owner=request.user) | Salary.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = salaries.values()
        return JsonResponse(list(data), safe=False)


def salary_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Salaries' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Source', 'Description', 'Date'])

    salaries = Salary.objects.filter(owner=request.user)

    for salary in salaries:
        writer.writerow([salary.amount, salary.source, salary.description, salary.date])

    return response


def salary_stats_view(request):
    return render(request, 'salary/salary-stat.html')


def salary_summary(request):
    current_date = datetime.date.today()
    three_months_ago = current_date-datetime.timedelta(days=30*3)
    salaries = Salary.objects.filter(owner=request.user, date__gte=three_months_ago, date__lte=current_date)
    summary = {}

    def get_salary_source(salary):
        return salary.source
    source_list = list(set(map(get_salary_source, salaries)))

    def get_salary_source_amount(source):
        amount = 0
        filtered_by_source = salaries.filter(source=source)

        for item in filtered_by_source:
            amount += item.amount

        return amount

    for x in salaries:
        for y in source_list:
            summary[y] = get_salary_source_amount(y)

    return JsonResponse({ 'salary_source_data': summary }, safe=False)
