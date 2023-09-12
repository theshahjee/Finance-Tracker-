from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User



# For Income Categories
class IncomeCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
# For Expense Categories
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Income(models.Model):
    name= models.CharField(max_length=50)
    date = models.DateTimeField(default=datetime.now())
    amount= models.FloatField()
    category = models.ForeignKey(IncomeCategory, related_name='income_catg', on_delete=models.CASCADE)
    note=models.TextField()

    def __str__(self):
        return f"Income of Rs.{self.amount} for {self.name}"


class Expense(models.Model):
    name= models.CharField(max_length=50)
    date = models.DateTimeField(default=datetime.now())
    amount= models.FloatField()
    category = models.ForeignKey(ExpenseCategory, related_name='expense_catg', on_delete=models.CASCADE)
    note=models.TextField()

    def __str__(self):
        return f"Rs.{self.amount} spent for {self.name}"
