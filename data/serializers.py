import calendar
from rest_framework import serializers
from .models import *

class SupermarketSalesSerializer(serializers.ModelSerializer):

    gender = serializers.SlugRelatedField(
        queryset=Gender.objects.all(),
        slug_field='name',
    )

    country = serializers.SlugRelatedField(
        queryset=Country.objects.all(),
        slug_field='name',
    )

    customer_type = serializers.SlugRelatedField(
        queryset=CustomerType.objects.all(),
        slug_field='name',
    )

    branch = serializers.SlugRelatedField(
        queryset=Branch.objects.all(),
        slug_field='name',
    )

    product_line = serializers.SlugRelatedField(
        queryset=ProductLine.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = SupermarketSales
        fields = '__all__'

class BranchDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(source = 'branch')
    label = serializers.CharField(source = "branch__name")
    value = serializers.IntegerField(source = 'quantity')
    percentage= serializers.DecimalField(max_digits=10, decimal_places=2)

class GenderDataSerializer(serializers.Serializer): 
    id = serializers.IntegerField(source='gender')
    label = serializers.CharField(source= 'gender__name')
    value = serializers.IntegerField(source='quantity')


class ProductBranchDataSerializer(serializers.Serializer): 
    product_line__name = serializers.CharField()
    quantityBranchA = serializers.IntegerField()
    quantityBranchB = serializers.IntegerField()
    quantityBranchC = serializers.IntegerField()


class CountryDataSerializer(serializers.Serializer):
    date__month = serializers.CharField()
    quantityNetherlands = serializers.IntegerField()
    quantityGermany = serializers.IntegerField()
    quantityFrance = serializers.IntegerField()
    month_name = serializers.SerializerMethodField()

    def get_month_name(self, obj):
        month_number = int(obj['date__month'])
        
        return calendar.month_name[month_number]
    
