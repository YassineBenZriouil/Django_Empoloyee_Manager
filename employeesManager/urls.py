from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add/', views.add_employee, name='add_employee'),
    path('update/<str:pk>/', views.update_employee, name='update_employee'),  # Changed to <str:pk>
    path('delete/<str:pk>/', views.delete_employee, name='delete_employee'),  # Changed to <str:pk>
    path('home/', views.home, name='home'),
]