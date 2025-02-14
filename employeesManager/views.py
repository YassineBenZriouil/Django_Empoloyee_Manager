from django.http import HttpResponse
from django.shortcuts import render, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from .forms import EmployeeForm
from datetime import datetime, date

client = MongoClient('mongodb://localhost:27017/')
db = client['employeesDB']
collection = db['employeesManager_employee']

def home(request):
    return HttpResponse("Welcome to the homepage!")

def employee_list(request):
    query = {}

    position_filter = request.GET.get('position')
    if position_filter:
        query['position'] = {'$regex': position_filter, '$options': 'i'}

    department_filter = request.GET.get('department')
    if department_filter:
        query['department'] = {'$regex': department_filter, '$options': 'i'}

    salary_min = request.GET.get('salary_min')
    salary_max = request.GET.get('salary_max')
    if salary_min:
        query['salary'] = {'$gte': float(salary_min)}
    if salary_max:
        if 'salary' in query:
            query['salary']['$lte'] = float(salary_max)
        else:
            query['salary'] = {'$lte': float(salary_max)}

    search_query = request.GET.get('search')
    if search_query:
        query['$or'] = [
            {'name': {'$regex': search_query, '$options': 'i'}},
            {'position': {'$regex': search_query, '$options': 'i'}},
            {'department': {'$regex': search_query, '$options': 'i'}}
        ]

    employees = list(collection.find(query))
    return render(request, 'employee_list.html', {'employees': employees})

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee_data = form.cleaned_data
            if 'hire_date' in employee_data and isinstance(employee_data['hire_date'], date):
                employee_data['hire_date'] = datetime.combine(
                    employee_data['hire_date'], datetime.min.time()
                )
            collection.insert_one(employee_data)
            return redirect('employee_list')
        else:
            print(form.errors)
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})

def update_employee(request, pk):
    employee_id = ObjectId(pk)
    employee = collection.find_one({'_id': employee_id})
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            updated_data = form.cleaned_data
            
            # Convert date fields to datetime
            if 'hire_date' in updated_data and isinstance(updated_data['hire_date'], date):
                updated_data['hire_date'] = datetime.combine(
                    updated_data['hire_date'], datetime.min.time()
                )
            
            collection.update_one({'_id': employee_id}, {'$set': updated_data})
            return redirect('employee_list')
    else:
        form = EmployeeForm(initial=employee)
    
    return render(request, 'update_employee.html', {'form': form})


def delete_employee(request, pk):
    employee_id = ObjectId(pk)
    if request.method == 'POST':
        collection.delete_one({'_id': employee_id})
        return redirect('employee_list')
    employee = collection.find_one({'_id': employee_id})
    return render(request, 'delete_employee.html', {'employee': employee})
