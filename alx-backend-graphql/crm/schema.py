import graphene
from graphene_django.types import DjangoObjectType
from .models import Customer, Product, Order
from django.core.exceptions import ValidationError
from django.db import transaction
import re

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        