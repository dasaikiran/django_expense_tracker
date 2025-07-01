from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TrackingHistory, CurrentBalance
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver 
from django.db.models import Count, Sum, Avg, Max, Min


# Create your views here.
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1!=password2:
            messages.error(request,"The passwords don't match")
            return redirect('register')

        if User.objects.filter(username = username).exists():
            messages.error(request,"The username already exists")
            return redirect('register')
        
        user = User.objects.create(
            username = username,
            email = email,
        )
        user.set_password(password1)
        user.save()
        messages.success(request,"Your Account is Successfully Registered")
        return redirect('login')

    return render(request,'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url="login")
def index(request):
    if request.method == "POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        current_balance,_ = CurrentBalance.objects.get_or_create(id = 1)
        expense_type = "CREDIT"
        if float(amount)<0:
            expense_type = "DEBIT"
        
        tracking_history = TrackingHistory.objects.create(
            amount = amount,
            expense_type = expense_type,
            current_balance = current_balance,
            description = description
        )
        current_balance.current_balance += float(tracking_history.amount)
        current_balance.save()
        return redirect('/')
    current_balance = TrackingHistory.objects.aggregate(current_balance = Sum('amount'))['current_balance']
    income = TrackingHistory.objects.filter(expense_type = "CREDIT").aggregate(income = Sum('amount'))['income']
    expense = TrackingHistory.objects.filter(expense_type = "DEBIT").aggregate(expense = Sum('amount'))['expense']
    if current_balance is None:
        current_balance = 0
    if income is None:
        income = 0
    if expense is None:
        expense = 0
    context = {'income': income, 'expense': expense, 'transactions' : TrackingHistory.objects.all(),'current_balance': current_balance}
    return render(request, 'index.html',context)

@receiver(post_save, sender = TrackingHistory)
def history_obj_created(sender, instance, created, **kwargs):
    print("History Created")

@receiver(post_delete, sender = TrackingHistory)
def history_obj_created(sender, instance, **kwargs):
    print("History Deleted")

def delete(request, id):
    transaction_obj = TrackingHistory.objects.get(id=id)
    if transaction_obj:
        transaction_obj.current_balance.current_balance -= transaction_obj.amount
        transaction_obj.current_balance.save()
        transaction_obj.delete()
    return redirect('/')