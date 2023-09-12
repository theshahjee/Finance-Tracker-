from django.contrib import admin
from .models import IncomeCategory,ExpenseCategory,Income,Expense

# Register your models here.
admin.site.register(IncomeCategory)
admin.site.register(ExpenseCategory)

# TO Modify INcome page for admin
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['name','date','amount','category','note']
    search_fields = ('name', 'category')
    list_filter = ('category','date')
admin.site.register(Income, IncomeAdmin)

# TO Modify Expenses page for admin
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['name','date','amount','category','note']
    search_fields = ('name', 'category')
    list_filter = ('category','date')
admin.site.register(Expense, ExpenseAdmin)