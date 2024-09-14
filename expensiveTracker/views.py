from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import PaymentMethodForm, TransactionForm
from .models import PaymentDetail, Transaction
from django.contrib import messages
from django.http import Http404


@login_required(login_url='/login')
def home(request):
    transactions = Transaction.objects.filter(user=request.user)
    current_page = int(request.GET.get('page', 1))
    page_data = 10
    total_data = len(transactions)
    total_page = len(transactions) // page_data
    prev_page = None
    next_page = None
    data_start = (page_data * current_page) - page_data
    data_end = page_data * current_page
    transactions = transactions[data_start: data_end]
    if total_data > data_end:
        next_page = current_page + 1
    if current_page > 1:
        prev_page = current_page - 1
    pages = range(1, total_page + 1)
    sno_start = data_start + 1
    context = {
        'current_page': current_page,
        'next_page': next_page,
        'prev_page': prev_page,
        'total_page': total_page,
        'total_data': total_data,
        'pages': pages,
        'transactions': transactions,
        'sno_start': sno_start,
    }

    return render(request, 'home.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='/login')
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login')
def add_payment_method(request):
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PaymentMethodForm(user=request.user)
    return render(request, 'add_payment_method.html', {'form': form})

@login_required(login_url='/login')
def add_transaction(request):
    payment_methods = PaymentDetail.objects.filter(user=request.user)
    if not payment_methods:
        messages.error(request, 'You need to add a payment method before creating a transaction.')
        return redirect('add_payment_method')
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'add_transaction.html', {'form': form})

@login_required(login_url='/login')
def transaction(request, id):
    try:
        transaction = Transaction.objects.get(id=id, user=request.user)
    except:
        transaction = None
    return render(request, 'transaction.html', {'transaction': transaction})
