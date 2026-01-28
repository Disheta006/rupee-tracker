from django.contrib import admin
from django.urls import path, include
from .import views
from .cycle_language import cycle_language

urlpatterns = [
    path('cycle_language/',cycle_language,name='cycle_language'),
    path('',views.index,name="index"),
    path('signup',views.signup,name="signup"),
    path('login_page',views.login_page,name="login_page"),
    path('reset/<uidb64>/<token>',views.CustomerPasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('password_reset_form/',views.password_reset_form,name="password_reset_form"),
    path('home/',views.home,name="home"),
    path('about',views.about,name="about"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('add_expense',views.add_expense,name="add_expense"),
    path('edit_expense/<int:id>/',views.edit_expense,name="edit_expense"),
    path('delete_expense/<int:id>/',views.delete_expense,name="delete_expense"),
    path('analysis',views.analysis,name="analysis"),
    path('category',views.category,name="category"),
    path('charts',views.charts,name="charts"),
    path('calender/',views.calender,name="calender"),
    path('calender/data/',views.calender_data,name="calender_data"),
    path('contact',views.contact,name="contact"),
    path('export/csv/',views.export_csv,name="export_csv"),
    path('export/pdf/',views.export_pdf,name="export_pdf"),
    path('delete_all_data/',views.delete_all_data,name="delete_all_data"),
    path('setting',views.setting,name="setting"),
    path('logout/',views.logout_view,name="logout"),
]