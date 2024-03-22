from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import CompanyDetails

@shared_task(bind=True)
def run_spider(self):
    from .views import emmision_spider,innovation_spider,resource_spider,human_spider,product_spider,workforce_spider,community_spider,management_spider,shareholder_spider,csr_spider
    for company in CompanyDetails.objects.all():
        emmision_spider(company.company_name)


    for company in CompanyDetails.objects.all():
        innovation_spider(company.company_name)


    for company in CompanyDetails.objects.all():
        resource_spider(company.company_name)



    for company in CompanyDetails.objects.all():
        human_spider(company.company_name)



    for company in CompanyDetails.objects.all():
        product_spider(company.company_name)


    for company in CompanyDetails.objects.all():
        workforce_spider(company.company_name)


    for company in CompanyDetails.objects.all():
        community_spider(company.company_name)


    for company in CompanyDetails.objects.all():
        management_spider(company.company_name)


    for company in CompanyDetails.objects.all():
        shareholder_spider(company.company_name)        



    for company in CompanyDetails.objects.all():
        csr_spider(company.company_name)     

    return "Done"   