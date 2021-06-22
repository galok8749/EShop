from store.models.product import Product
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models.product import Product
# Create your views here.


def index(request):
    products = Product.get_all_products()
    # print(products)
    return render(request, 'index.html', {'products' : products})