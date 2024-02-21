# esg_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('get_company_symbol/', views.get_company_symbol,name="get_company_symbol"),
    path('get_company_esg_sector/', views.get_company_esg_sector,name="get_company_esg_sector"),
    path('get_company_details/', views.get_company_details,name="get_company_details"),
    path('spider/', views.get_company_name_for_spider, name='run_spider'),
    path('get_esg_score', views.get_esg_score, name='get_esg_score'),
    path('emission_spider/', views.emmision_spider, name='emission_spider'),
    path('innovation_spider/', views.innovation_spider, name='innovation_spider'),
    path('resource_spider/', views.resource_spider, name='innovation_spider'),
    path('human_spider/', views.human_spider, name='human_spider'),
    path('product_spider/', views.product_spider, name='product_spider'),
    path('workforce_spider/', views.workforce_spider, name='workforce_spider'), 
    path('community_spider/', views.community_spider, name='community_spider'), 
    path('management_spider/', views.management_spider, name='management_spider'),
    path('shareholder_spider/', views.shareholder_spider, name='shareholder_spider'),
    path('csr_spider/', views.csr_spider, name='csr_spider'), 
]
