from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('supermarket-sales', SupermarketSalesViewset, basename='supermarket-sales')
router.register('branch-data', BranchDataViewset, basename='branch-data')
router.register('gender-data',GenderDataViewset, basename='gender-data')
router.register('productbranchdata',ProductBranchViewset, basename='productbranchdata')
router.register('country-data',CountryDataViewset, basename='country-data')
    
urlpatterns = router.urls

