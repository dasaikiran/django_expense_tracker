from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CurrentBalance(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    current_balance = models.FloatField(default=0)

    def __str__(self):
        return str(self.current_balance)

class TrackingHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    current_balance = models.ForeignKey(CurrentBalance, on_delete=models.CASCADE)
    amount = models.FloatField()
    expense_type = models.CharField(max_length=10,choices=(("CREDIT","CREDIT"),("DEBIT","DEBIT")))
    description = models.CharField(max_length= 200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description} & {str(self.amount)} {self.expense_type}"
    
class RequestLogs(models.Model):
    request_info = models.TextField()
    request_type = models.CharField(max_length=100)
    request_path = models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)