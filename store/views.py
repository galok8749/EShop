from django import http
from store.models.product import Product
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from .models.product import Product
from .models.category import Category
from .models.customer import Customer

# Create your views here.

def index(request):
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()
    data = {}
    data['products'] = products
    data['categories'] = categories
    return render(request, 'index.html', data)

def validateCustomer(customer):
    error_message = None

    if (not customer.first_name):
        error_message = 'First Name Required !!!'
    elif len(customer.first_name) < 4:
        error_message = 'First Name must be at least 4 char long'
    elif (not customer.last_name):
        error_message = 'Last Name Required !!!'
    elif len(customer.last_name) < 4:
        error_message = 'Last Name must be at least 4 char long'
    elif (not customer.phone):
        error_message = 'phone required'
    elif len(customer.phone) < 10:
        error_message = 'phone number must be 10 char long'
    elif len(customer.password) < 6:
        error_message = 'password must be 6 char long'
    elif len(customer.email) < 5:
        error_message = 'email must be 5 char long'
    elif customer.isExits():
        error_message = 'Email already registered !!!'
    
    return error_message

def registerUser(request):
    postData = request.POST
    first_name = postData.get('firstname')
    last_name = postData.get('lastname')
    phone = postData.get('phone')
    email = postData.get('email')
    password = postData.get('password')

    # store customer data
    value = {
        'first_name' : first_name,
        'last_name' : last_name,
        'phone' : phone,
        'email' : email
    }

    customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
    # validate customer
    error_message =  validateCustomer(customer)
   
    # saving
    if not error_message:
        customer.password = make_password(customer.password)
        customer.register()
        return redirect('homepage')
    else:
        data = {
            'error' : error_message,
            'values' : value
        }
        return render(request, 'signup.html', data)

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        return registerUser(request)
    

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        
        error_message = None
        if customer:
            flag =  check_password(password, customer.password)
            if flag:
                return redirect('homepage')
            else:
                error_message = 'Email or Password invalid !!!'
        else:
            error_message = 'Email or Password invalid !!!'

        return render(request, 'login.html', {'error' : error_message})