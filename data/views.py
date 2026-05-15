from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.db.models import Case, IntegerField, Sum, F, Func, Value, FloatField, When, When
from django.db.models.functions import Cast

# Create your views here.
class SupermarketSalesViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = SupermarketSales.objects.all()
    serializer_class = SupermarketSalesSerializer

    def list(self, request):
        queryset = SupermarketSales.objects.all()
        serializer = SupermarketSalesSerializer(queryset, many=True)
        return Response(serializer.data)
    
class BranchDataViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = SupermarketSales.objects.all()
    serializer_class = BranchDataSerializer

    def list(self, request):
        total_sum = SupermarketSales.objects.aggregate(total_quantity=Sum('quantity'))
        total_quantity_value = total_sum['total_quantity']

        queryset = SupermarketSales.objects.values('branch', 'branch__name')\
        .annotate(quantity = Sum('quantity'))\
        .annotate(percentage = Func(
            (Cast(F('quantity'), FloatField())/total_quantity_value)*100,
            Value=(2),
            function="ROUND",
            output_field=FloatField()
        ))

        serializer = BranchDataSerializer(queryset, many=True)
        return Response(serializer.data)
    
class GenderDataViewset(viewsets.ViewSet): 
    permission_classes = [permissions.AllowAny]
    queryset = SupermarketSales.objects.all()
    serializer_class = GenderDataSerializer

    def list(self, request): 
        queryset = SupermarketSales.objects.values('gender', 'gender__name')\
                   .annotate(quantity=Sum('quantity'))
        
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
class ProductBranchViewset(viewsets.ViewSet): 
    permission_classes = [permissions.AllowAny]
    queryset = SupermarketSales.objects.all()
    serializer_class = ProductBranchDataSerializer

    def list(self, request): 
        queryset = SupermarketSales.objects.values('product_line__name')\
                   .annotate(quantityBranchA=Sum(
                       Case(
                           When(branch__name="A", then='quantity'),
                           default=0, 
                           output_field=IntegerField()
                       )
                   ))\
                   .annotate(quantityBranchB=Sum(
                       Case(
                           When(branch__name="B", then='quantity'),
                           default=0, 
                           output_field=IntegerField()
                       )
                   ))\
                   .annotate(quantityBranchC=Sum(
                       Case(
                           When(branch__name="C", then='quantity'),
                           default=0, 
                           output_field=IntegerField()
                       )
                   ))
        
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    

class CountryDataViewset(viewsets.ViewSet): 
    permission_classes = [permissions.AllowAny]
    queryset = SupermarketSales.objects.all()
    serializer_class = CountryDataSerializer

    def list(self, request): 
        queryset = SupermarketSales.objects.values('date__month')\
                   .annotate(quantityNetherlands=Sum(
                       Case(
                           When(country__name="Netherlands", then='quantity'),
                           default=0, 
                           output_field=IntegerField()
                       )
                   ))\
                   .annotate(quantityGermany=Sum(
                       Case(
                           When(country__name="Germany", then='quantity'),
                           default=0, 
                           output_field=IntegerField()
                       )
                   ))\
                   .annotate(quantityFrance=Sum(
                       Case(
                           When(country__name="France", then='quantity'),
                           default=0, 
                           output_field=IntegerField()
                       )
                   ))
        
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)