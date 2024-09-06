from django.shortcuts import render
from rest_framework import viewsets

from mill.models import Customer, Product
from mill.serializers import CustomerSerialzer, ProductSerialzer
# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerialzer
    queryset = Product.objects.all()


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerialzer
    queryset = Customer.objects.all()
