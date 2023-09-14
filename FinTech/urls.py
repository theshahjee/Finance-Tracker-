
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard',views.dashboard,name="dashboard"),
    path('incomes',views.income,name="incomes"),
    path('expenses',views.expenses,name="expenses"),

    path('edit-income/<int:id>',views.edit_income,name="edit-income"),
    path('edit-expense/<int:id>',views.edit_expense,name="edit-expense"),

    path('delete-expense/<int:id>',views.delete_expense,name="delete-expense"),
    path('delete-income/<int:id>',views.delete_income,name="delete-income"),

    path('expense-report/<str:duration>',views.expense_report, name="expense-report"),
    path('income-report/<str:duration>',views.income_report, name="income-report"),

    path('',views.index,name="index"),
    path('signup',views.signup,name="signup"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),
]
