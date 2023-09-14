from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User, auth 
from datetime import date
from .models import Expense,Income,IncomeCategory,ExpenseCategory,Account,Budget
# Create your views here.

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        my_account= Account.objects.get(user=request.user.id)
        balance= my_account.balance
        return render(request,"dashboard.html",{"balance":balance})
    else:
        return redirect("/")

# Income
def income(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            name=request.POST['name']
            category_id=request.POST.get('category')
            amount=request.POST['amount']
            date=request.POST['date']
            note=request.POST.get('note')
            category = IncomeCategory.objects.get(id=int(category_id))

            my_account= Account.objects.get(user=User.objects.get(id = request.user.id))
            my_account.balance+=float(amount)
            my_account.save()
            print("Account Balance Updated!!")
            # Create INcome record
            Income.objects.create(name=name,user=User.objects.get(id = request.user.id),category=category,amount=amount,date=date,note=note)
            return redirect('/incomes')

        incomes_catg= IncomeCategory.objects.all()
        incomes= Income.objects.filter(user=request.user.id)

        return render(request,"income.html",{"categories":incomes_catg,"incomes":incomes})
    else:
        return redirect("/")

# Expenses
def expenses(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            name=request.POST['name']
            category_id=request.POST.get('category')
            amount=request.POST['amount']
            date=request.POST['date']
            note=request.POST.get('note')
            category = ExpenseCategory.objects.get(id=int(category_id))

            my_account= Account.objects.get(user=User.objects.get(id = request.user.id))
            my_account.balance-=float(amount)
            my_account.save()
            print("Account Balance Updated!!")
            # Create Expenses record
            Expense.objects.create(name=name,user=User.objects.get(id = request.user.id),category=category,amount=amount,date=date,note=note)
            return redirect('/expenses')

        expenses_catg= ExpenseCategory.objects.all()
        expenses= Expense.objects.filter(user=request.user.id)

        return render(request,"expense.html",{"categories":expenses_catg,"expenses":expenses})
    else:
        return redirect("/")


# EDIT Income
def edit_income(request,id):
    if request.user.is_authenticated:
        income=Income.objects.get(id=id)
        if request.method=="POST":
            name=request.POST['name']
            category_id=request.POST.get('category')
            amount=request.POST['amount']
            date=request.POST['date']
            note=request.POST.get('note')
            category = IncomeCategory.objects.get(id=int(category_id))

            # Update Account Balance
            my_account= Account.objects.get(user=User.objects.get(id = request.user.id))
            if float(amount)<income.amount:
                my_account.balance-=float((income.amount-float(amount)))
            else:
                my_account.balance+=float((float(amount)-income.amount))
            
            my_account.save()
            print("Account balance updated")

            # Update income 
            income.name=name
            income.amount=float(amount)
            if date:
                income.date=date
            income.note=note
            income.category=category
            income.save()
            print("Income Details Updated")
            return redirect("/incomes")

        categories= IncomeCategory.objects.all()
        return render(request,"income_edit.html",{"income":income,"categories":categories})
    else:
        return redirect("/")

# EDIT Expense
def edit_expense(request,id):
    if request.user.is_authenticated:
        expense=Expense.objects.get(id=id)
        if request.method=="POST":
            name=request.POST['name']
            category_id=request.POST.get('category')
            amount=request.POST['amount']
            date=request.POST['date']
            note=request.POST.get('note')
            category = ExpenseCategory.objects.get(id=int(category_id))

            # Update Account Balance
            my_account= Account.objects.get(user=User.objects.get(id = request.user.id))
            if float(amount)<expense.amount:
                my_account.balance+=float((expense.amount-float(amount)))
            else:
                my_account.balance-=float((float(amount)-expense.amount))
            
            my_account.save()
            print("Account balance updated")

            # Update expense 
            expense.name=name
            expense.amount=float(amount)
            if date:
                expense.date=date
            expense.note=note
            expense.category=category
            expense.save()
            print("expense Details Updated")
            return redirect("/expenses")

        categories= ExpenseCategory.objects.all()
        return render(request,"expense_edit.html",{"expense":expense,"categories":categories})
    else:
        return redirect("/")


# Delete Expense
def delete_expense(request,id):
    if request.user.is_authenticated:
        expense=Expense.objects.get(id=id)
        my_account= Account.objects.get(user=User.objects.get(id = request.user.id))
        my_account.balance+=float(expense.amount)
        my_account.save()
        print("Account balance updated")

        Expense.objects.get(id=id).delete()
        print("Expense deleted")
        return redirect("/expenses")
    else:
        return redirect("/")
    
# Delete Incmoe
def delete_income(request,id):
    if request.user.is_authenticated:
        income=Income.objects.get(id=id)
        my_account= Account.objects.get(user=User.objects.get(id = request.user.id))
        my_account.balance-=float(income.amount)
        my_account.save()
        print("Account balance updated")

        Income.objects.get(id=id).delete()
        print("Income Deleted")
        return redirect("/incomes")
    else:
        return redirect("/")


# Index page
def index(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        return render(request, "index.html",{})

# Signup 
def signup(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            first_name= request.POST['first_name']
            last_name= request.POST['last_name']
            email= request.POST['email']
            password= request.POST['password']

            if User.objects.filter(username=email).exists():
                print("Username is already used")
                return redirect('/')
            else:
                user = User.objects.create_user(username=email,password= password, email=email, first_name=first_name,last_name=last_name)
                user.save()
                print("User Account created successfully")
                # Create Account for users
                Account.objects.create(user=user,balance=0,details="Primary account for User="+str(user.id),name=f'Account for {user.id}-{first_name}')
                print("Users Account Created!!")

                return redirect('/')
        return render(request,"index.html",{})
    else:
        return redirect("/dashboard")
    
# Login
def login(request):
    if request.method== "POST":
        username = request.POST['email']
        password = request.POST['password']

        user= auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            print(f"User {username} is logged in")
            return redirect("/dashboard")
        else:
            print("Invalid Login details")
            return redirect("/")
    else:
        return render(request, "/",{})


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect("/")