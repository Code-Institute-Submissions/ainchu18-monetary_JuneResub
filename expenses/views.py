from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
import datetime
import csv


@login_required(login_url='/accounts/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_num = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_num)

    context = {
        'expenses': expenses,
        'page_obj': page_obj
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/accounts/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)

        if not date:
            messages.error(request, 'Expense date is required')
            return render(request, 'expenses/add_expense.html', context)

        if not category:
            messages.error(request, 'Category is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, amount=amount,
                               date=date, category=category, description=description)
        messages.success(request, 'Expense saved successfully')
        return redirect('expenses')


@login_required(login_url='/accounts/login')
def expense_edit(request, id):
    categories = Category.objects.all()
    expense = Expense.objects.get(pk=id)
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)

        if not date:
            messages.error(request, 'Expense date is required')
            return render(request, 'expenses/add_expense.html', context)

        if not category:
            messages.error(request, 'Category date is required')
            return render(request, 'expenses/add_expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description

        expense.save()

        messages.success(request, 'Expense updated successfully')
        return redirect('expenses')

        messages.info(request, 'Editing expense, please wait')
        return render(request, 'expenses/edit-expense.html', context)


@login_required(login_url='/accounts/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully')
        return redirect('expenses')
    return render(request, 'expenses/delete-expense.html')


@login_required(login_url='/accounts/login')
def search_expense(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/accounts/login')
def export_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Category', 'Description', 'Date'])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.category, expense.description, expense.date])

    return response


@login_required(login_url='/accounts/login')
def stats_view(request):
    return render(request, 'expenses/stats.html')


@login_required(login_url='/accounts/login')
def expense_category_summary(request):
    current_date = datetime.date.today()
    three_months_ago = current_date-datetime.timedelta(days=30*3)
    expenses = Expense.objects.filter(owner=request.user, date__gte=three_months_ago, date__lte=current_date)
    summary = {}

    def get_expense_category(expense):
        return expense.category
    category_list = list(set(map(get_expense_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount

        return amount

    for x in expenses:
        for y in category_list:
            summary[y] = get_expense_category_amount(y)

    return JsonResponse({ 'expense_category_data': summary }, safe=False)