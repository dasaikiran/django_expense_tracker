from django.contrib import admin
from .models import TrackingHistory,CurrentBalance

# Register your models here.

admin.site.register(CurrentBalance)

@admin.action(description="Mark selected obj expense_type as Debit")
def make_debit(modeladmin, request, queryset):
    for q in queryset:
        obj = TrackingHistory.objects.get(id=q.id)
        if obj.amount > 0:
            obj.amount = obj.amount * -1
            obj.save()
    queryset.update(expense_type="DEBIT")

@admin.action(description="Mark selected obj expense_type as Credit")
def make_credit(modeladmin, request, queryset):
    for q in queryset:
        obj = TrackingHistory.objects.get(id=q.id)
        if obj.amount < 0:
            obj.amount = obj.amount * -1
            obj.save()
    queryset.update(expense_type="CREDIT")
class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = [
        "current_balance",
        "amount",
        "expense_type",
        "description",
        "created_at"
    ]
    actions=[make_debit,make_credit]
    search_fields=[
        'expense_type','description'
    ]
    list_filter=['expense_type']
    ordering=['-created_at']

admin.site.register(TrackingHistory,TrackingHistoryAdmin)