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


@login_required(login_url='/accounts/login')
def add_saving(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'saving/add_saving.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'saving/add_saving.html', context)
        description = request.POST['description']
        date = request.POST['saving_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'saving/add_saving.html', context)

        if not date:
            messages.error(request, 'Savings date is required')
            return render(request, 'saving/add_saving.html', context)

        if not source:
            messages.error(request, 'Source is required')
            return render(request, 'saving/add_saving.html', context)

        Saving.objects.create(owner=request.user, amount=amount,
                               date=date, source=source, description=description)
        messages.success(request, 'Savings saved successfully')
        return redirect('saving')


@login_required(login_url='/accounts/login')
def saving_edit(request, id):
    saving = Saving.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'saving': saving,
        'values': saving,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'saving/edit-saving.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'saving/edit-saving.html', context)
        description = request.POST['description']
        date = request.POST['saving_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'saving/add_saving.html', context)

        if not date:
            messages.error(request, 'Savings date is required')
            return render(request, 'saving/add_saving.html', context)

        if not source:
            messages.error(request, 'Source is required')
            return render(request, 'saving/add_saving.html', context)

        saving.amount = amount
        saving.date = date
        saving.source = source
        saving.description = description

        saving.save()

        messages.success(request, 'Savings updated successfully')
        return redirect('saving')

        messages.info(request, 'Editing savings, please wait')
        return render(request, 'saving/edit-saving.html', context)


@login_required(login_url='/accounts/login')
def delete_saving(request, id):
    saving = Saving.objects.get(pk=id)
    if request.method == 'POST':
        saving.delete()
        messages.success(request, 'Savings deleted successfully')
        return redirect('saving')
    return render(request, 'saving/delete-saving.html')


def search_saving(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        savings = Saving.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Saving.objects.filter(
            date__istartswith=search_str, owner=request.user) | Saving.objects.filter(
            description__icontains=search_str, owner=request.user) | Saving.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = savings.values()
        return JsonResponse(list(data), safe=False)


def saving_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Savings' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Source', 'Description', 'Date'])

    savings = Saving.objects.filter(owner=request.user)

    for saving in savings:
        writer.writerow([saving.amount, saving.source, saving.description, saving.date])

    return response