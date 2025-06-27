from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TrackingHistory, CurrentBalance

# Create your views here.

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
    current_balance,_ = CurrentBalance.objects.get_or_create(id = 1)
    income = 0
    expense = 0
    for transaction in TrackingHistory.objects.all():
        if transaction.expense_type == "DEBIT":
            expense += transaction.amount
        else:
            income += transaction.amount
    context = {'income': income, 'expense': expense, 'transactions' : TrackingHistory.objects.all(),'current_balance': current_balance}
    return render(request, 'index.html',context)

def delete(request, id):
    transaction_obj = TrackingHistory.objects.get(id=id)
    if transaction_obj:
        transaction_obj.current_balance.current_balance -= transaction_obj.amount
        transaction_obj.current_balance.save()
        transaction_obj.delete()
    return redirect('/')