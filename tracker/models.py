from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Expense(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}-{self.description}"
    CATEGORY_CHOICES = (
        ('Food',_('Food')),
        ('Shopping',_('Shopping')),
        ('Housing',_('Housing')),
        ('Transport',_('Transport')),
        ('Entertainment',_('Entertainment')),
        ('Health',_('Health')),
        ('Others',_('Others')),
    )
    title = models.CharField(max_length=100)
    amount = models.FloatField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True,null=True)
    def __str__(self):
        return f"{self.title}-{self.amount}"
    
class UserSettings(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    monthly_income = models.FloatField(default=50000)
    spending_threshold = models.PositiveSmallIntegerField(default=70)
    billing_cycle_start = models.PositiveSmallIntegerField(default=1)
    hide_amounts = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username} settings"
    
class ContactMessage(models.Model):
    CATEGORY_CHOICES = [
        ('feedback',_("General Feedback")),
        ('issue',_("Technical Issue")),
        ('features',_("Feature Request")),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}-{self.category}"