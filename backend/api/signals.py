from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EsgScore, CompanyDetails, Sector

# Signal handler for when an EsgScore instance is created
@receiver(post_save, sender=EsgScore)
def esg_score_created(sender, instance, created, **kwargs):
    if created:
        instance.save()
        print(f'EsgScore instance {instance.id} has been created.')

# Signal handler for when a CompanyDetails instance is created
@receiver(post_save, sender=CompanyDetails)
def company_details_created(sender, instance, created, **kwargs):
    if created:
        instance.save()
        print(f'CompanyDetails instance {instance.id} has been created.')

# Signal handler for when a Sector instance is created
@receiver(post_save, sender=Sector)
def sector_created(sender, instance, created, **kwargs):
    if created:
        instance.save()
        print(f'Sector instance {instance.id} has been created.')