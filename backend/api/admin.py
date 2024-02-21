from django.contrib import admin
from .models import Sector,EsgScore,CompanyDetails
# Register your models here.
admin.site.register(Sector)
admin.site.register(EsgScore)
admin.site.register(CompanyDetails)