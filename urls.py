from django.urls import path
from . import views

urlpatterns = [
    path('',views.student_login,name='login'),
    path('result/', views.search_result, name='result'),
    path('download/<int:roll_no>/', views.download_result, name='download_result'),
    path('dashboard/',views.dashboard,name='dashboard')
]