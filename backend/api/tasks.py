from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .views import emmision_spider,innovation_spider,resource_spider,human_spider,product_spider,workforce_spider,community_spider,management_spider,shareholder_spider,csr_spider
from .models import CompanyDetails

@shared_task
def run_emission_spider():
    for company in CompanyDetails.objects.all():
        emmision_spider(company.company_name)

@shared_task
def run_innovation_spider():
    for company in CompanyDetails.objects.all():
        innovation_spider(company.company_name)

@shared_task
def run_resource_spider():
    for company in CompanyDetails.objects.all():
        resource_spider(company.company_name)


@shared_task
def run_human_spider():
    for company in CompanyDetails.objects.all():
        human_spider(company.company_name)


@shared_task
def run_product_spider():
    for company in CompanyDetails.objects.all():
        product_spider(company.company_name)

@shared_task
def run_workforce_spider():
    for company in CompanyDetails.objects.all():
        workforce_spider(company.company_name)

@shared_task
def run_community_spider():
    for company in CompanyDetails.objects.all():
        community_spider(company.company_name)

@shared_task
def run_management_spider():
    for company in CompanyDetails.objects.all():
        management_spider(company.company_name)

@shared_task
def run_shareholder_spider():
    for company in CompanyDetails.objects.all():
        shareholder_spider(company.company_name)        


@shared_task
def run_csr_spider():
    for company in CompanyDetails.objects.all():
        csr_spider(company.company_name)        