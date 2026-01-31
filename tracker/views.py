from datetime import date, datetime
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.shortcuts import redirect
from django.utils import translation
import json
from django.db.models import Sum, Count
from .models import Expense
from .models import UserSettings
from .models import ContactMessage
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.views import PasswordResetConfirmView
from .forms import CustomerSetPasswordForm
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.utils.translation import gettext_lazy as _

class CustomerPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomerSetPasswordForm
    template_name = 'password_reset_confirm.html'

# Create your views here.
def password_reset_form(request):
    return render(request,"tracker/registration/password_reset_form.html")

def index(request):
    return render(request,"tracker/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request,_("Passwords do not match!"))
            return redirect("signup")
        
        if User.objects.filter(username=username).exists():
            messages.error(request,_("Email already registered"))
            return redirect("signup")
        
        user = User.objects.create_user(
            username = username,
            email = email,
            password = password
        )
        user.save()
        messages.success(request,_("Account created successfully"))
        return redirect("login_page")
    return render(request,"tracker/signup.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")

        user = authenticate(
            request,
            username = username,
            password = password
        )
        
        if user is not None:
            login(request,user)

            if remember_me:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                request.session.set_expiry(0)

            return JsonResponse({
                "success":True,
                "redirect_url": "/home/"
                })
        
    return render(request,"tracker/login_page.html")

@never_cache
@login_required
def home(request):
    return render(request,"tracker/home.html")

def about(request):
    return render(request,"tracker/about.html")

@never_cache
@login_required
def dashboard(request):
    settings, created = UserSettings.objects.get_or_create(user=request.user)
    start_day = settings.billing_cycle_start
    today = date.today()
    if today.day >= start_day:
        cycle_start = date(today.year,today.month,start_day)
    else:
        if today.month == 1:
            cycle_start = date(today.year-1,12,start_day)
        else:
            cycle_start = date(today.year,today.month-1,start_day)
    cycle_expenses = Expense.objects.filter(
        user = request.user,
        date__gte = cycle_start
    )
    recent_expenses = Expense.objects.filter(
        user = request.user
    ).order_by('-created_at')[:5]
    total_expense_data = Expense.objects.filter(user=request.user).aggregate(amount_sum=Sum('amount'))
    amount_sum = total_expense_data['amount_sum'] or 0
    income_error = ''
    income_message = ''
    total_income = settings.monthly_income
    threshold = settings.spending_threshold
    if request.method == 'POST':
        try:
            total_income = float(request.POST.get('total_income'))
            request.session['total_income'] = total_income
        except ValueError:
            income_error = "#dc2626"
            income_message = _("Enter valid INCOME value!")
    else:
        total_income = settings.monthly_income
    
    health_percent = int((amount_sum/total_income)*100) if total_income > 0 else 0
    
    if amount_sum == 0:
        health_percent = 0
        health_color = "#8a918d"
        health_message = _("No expenses yet!")
    elif health_percent < threshold:
        health_color = "#16a34a"
        health_message = _("Your spending is under control 👍")
    elif health_percent < threshold+15:
        health_color = "#f97316"
        health_message = _("Warning! Your spending is approaching your threshold! ⚠️")
    else:
        health_color = "#dc2626"
        health_message = _("Danger! You have exceeded your budget 🚨")
    radius = 45
    circumference = 2*3.1416*radius
    dash_offset = circumference-(health_percent/100)*circumference
    context = {
        'expenses': recent_expenses,
        'income_error': income_error,
        'income_message': income_message,
        'total_expense': amount_sum,
        'total_income': total_income,
        'health_color' : health_color,
        'health_percent': round(health_percent),
        'health_message': health_message,
        'circumference' : circumference,
        'dash_offset' : dash_offset,
    }
    return render(request,'tracker/dashboard.html',context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        Expense.objects.create(
            user= request.user,
            title = request.POST['title'],
            amount = request.POST['amount'],
            category = request.POST['category'],
            date = request.POST['date']
        )
    return redirect('/dashboard/#recent-expenses')

def edit_expense(request,id):
    expenses = get_object_or_404(Expense,id=id)
    if request.method == 'POST':
        expenses.title = request.POST['title']
        expenses.amount = request.POST['amount']
        expenses.category = request.POST['category']
        expenses.date = request.POST['date']
        expenses.save()
        return redirect('/dashboard/#recent-expenses')
    return render(request,'tracker/edit_expense.html',{'expenses':expenses})

def delete_expense(request,id):
    expense = get_object_or_404(Expense,id=id)
    expense.delete()
    return redirect('/dashboard/#recent-expenses')

@login_required
def analysis(request):
    expenses = Expense.objects.filter(user=request.user)
    total_spent = expenses.aggregate(total=Sum('amount'))['total'] or 0
    transaction_count = expenses.count()
    average_spent = round(total_spent/transaction_count,2) if transaction_count else 0
    category_data = (
        expenses.values('category').annotate(total=Sum('amount')).order_by('-total')
    )
    categories = []
    for item in category_data:
        percent  = (item['total']/total_spent*100) if total_spent else 0
        categories.append({
            'name': item['category'],
            'total': float(item['total']),
            'percent': round(percent)
        })
    context = {
        'categories': categories,
        'transactions': transaction_count,
        'average_spent': average_spent,
    }
    return render(request,'tracker/analysis.html',context)

@login_required
def category(request):
    category_totals = (
        Expense.objects.filter(user=request.user).values('category').annotate(total=Sum('amount'))
    )
    category_data = {item['category']:item['total'] for item in category_totals}
    context = {
        'category_data': category_data
    }
    return render(request,"tracker/category.html",context)

@login_required
def charts(request):
    expenses = (
        Expense.objects.filter(user=request.user).values('category').annotate(total=Sum('amount'))
    )
    total_spent = sum(e['total'] for e in expenses) if expenses else 0
    categories = []
    for e in expenses:
        percent = (e['total']/total_spent*100) if total_spent else 0
        ICONS = {
            "Housing": 'fa-house',
            "Food": 'fa-utensils',
            "Shopping": 'fa-bag-shopping',
            "Transport": 'fa-car',
            "Health": 'fa-heart-pulse',
            "Entertainment": 'fa-film',
            "Other": 'fa-ellipsis',
        }
        categories.append({
            'name': e['category'],
            'amount': e['total'],
            'percent': round(percent,1),
            'icon': ICONS.get(e['category'],"fa-wallet"),
        })
    context = {
            'labels': json.dumps([c['name'] for c in categories]),
            'values': json.dumps([float(c['amount']) for c in categories]),
            'total_spent': total_spent,
            'categories' : categories,
        }
    return render(request,"tracker/charts.html",context)

@login_required
def calender_data(request):
    today = datetime.now()
    month = int(request.GET.get('month',today.month))
    year = int(request.GET.get('year',today.year))
    expenses = Expense.objects.filter(
        user = request.user,
        date__month = month,
        date__year = year,
    )
    expense_days = list(
        expenses.values_list('date__day',flat=True).distinct()
    )
    summary = expenses.aggregate(
        total_spent = Sum('amount'),
        transactions = Count('id')
    )
    return JsonResponse({
        'expense_days' : expense_days,
        'total_spent' : summary['total_spent'] or 0,
        'transactions' : summary['transactions']
    })

@login_required
def calender(request):
    return render(request,"tracker/calender.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        category = request.POST.get("category")
        message = request.POST.get("message")
        ContactMessage.objects.create(
            name = name,
            email = email,
            category = category,
            message = message
        )
        messages.success(request,_("Thank you! Your message has been sent."))
        return redirect('contact')

    return render(request,"tracker/contact.html")

@login_required
def export_csv(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title','Amount','Category','Date','Description'])
    for e in expenses:
        writer.writerow([e.title,e.amount,e.category,e.date,e.description or ""])
    return response

@login_required
def export_pdf(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expenses.pdf"'
    p = canvas.Canvas(response,pagesize=A4)
    width,height = A4
    y = height-50
    p.setFont("Helvetica-Bold",16)
    p.drawString(50,y,"Your Expenses")
    y -= 30
    p.setFont("Helvetica",12)
    p.drawString(50,y,"TItle")
    p.drawString(200,y,"Amount")
    p.drawString(300,y,"Category")
    p.drawString(400,y,"Date")
    y -= 20
    for e in expenses:
        if y < 50:
            p.showPage()
            y = height - 50
        p.drawString(50,y,str(e.title))
        p.drawString(200,y,str(e.amount))
        p.drawString(300,y,str(e.category))
        p.drawString(400,y,str(e.date))
        y -= 20
    p.showPage()
    p.save()
    return response

@login_required
def setting(request):
    settings, created = UserSettings.objects.get_or_create(user=request.user)
    if request.method == "POST":
        settings.monthly_income = float(request.POST.get("monthly_income"))
        settings.spending_threshold = int(request.POST.get("spending_threshold"))
        settings.billing_cycle_start = int(request.POST.get("billing_cycle_start"))
        settings.save()
        messages.success(request,_('Preferences updated successfully!'))

    return render(request,"tracker/setting.html",{"settings":settings})

@login_required
def delete_all_data(request):
    Expense.objects.filter(user=request.user).delete()
    return redirect('dashboard')

@login_required
def hide_amounts(request):
    try:
        security = request.user.usersettings
        security.hide_amounts = not security.hide_amounts
        security.save()
        return JsonResponse({
            'status':'success',
            'hide_amounts': security.hide_amounts
        })
    except Exception as e:
        return JsonResponse({
            "status":"error",
            "message":str(e)
        },status=500)
    
def logout_view(request):
    logout(request)
    messages.success(request,"You have been logged out successfully.")
    return redirect('login_page')

def cycle_language(request):
    languages = [lang[0] for lang in settings.LANGUAGES]
    current_lang = translation.get_language()

    try:
        next_lang = languages[(languages.index(current_lang) + 1) % len(languages)]
    except ValueError:
        next_lang = settings.LANGUAGE_CODE

    translation.activate(next_lang)
    request.session['django_language'] = next_lang

    return redirect(request.META.get('HTTP_REFERER', '/'))