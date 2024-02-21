# esg_app/models.py
import uuid
from django.db import models

class EsgScore(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    company = models.OneToOneField("CompanyDetails", on_delete=models.CASCADE,null=True,blank=True)
    polarity_score = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    environment_score = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    social_score = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    governance_score = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    emission = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    innovation = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    resource = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    human_rights = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    product_responsibility = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    workforce = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    community = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    management = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    shareholders = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    csr_strategy = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    
    def __str__(self):
        return self.company.company_name
    

    def save(self, *args, **kwargs):
        # Define the factors and corresponding attribute names
        factors = {
            'environment_score': ['emission', 'innovation', 'resource'],
            'social_score': ['human_rights', 'product_responsibility', 'workforce', 'community'],
            'governance_score': ['management', 'shareholders', 'csr_strategy'],
        }

        polarity_score = 0

        if self.company and self.company.sector:
            sector = self.company.sector

            for score, attribute_list in factors.items():
                calculated_score = 0
                for attr in attribute_list:
                    value = getattr(self, attr, 0)
                    sector_value = getattr(sector, attr, 0)
                    if value is not None and sector_value is not None:
                        calculated_score += value * sector_value

                setattr(self, score, calculated_score)
                polarity_score += calculated_score

            self.polarity_score = polarity_score

        super(EsgScore, self).save(*args, **kwargs)


class CompanyDetails(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    company_name = models.CharField(max_length=200,null=True,blank=True)
    sector = models.ForeignKey("Sector", on_delete=models.CASCADE)
    symbol = models.CharField(max_length=100,null=True,blank=True)
    url = models.URLField()
    logo = models.CharField(max_length=1000,null=True,blank=True)
    
    
    def __str__(self):
        return self.company_name




class Sector(models.Model):
    sector = models.CharField(max_length=200)
    environment_factor = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    social_factor = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    governance_factor = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    emission = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    innovation = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    resource = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    human_rights = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    product_responsibility = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    workforce = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    community = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    management = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    shareholders = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    csr_strategy = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)

    def __str__(self):
        return self.sector

    def save(self, *args, **kwargs):
        # Define the factors and corresponding attribute names
        factors = {
            'environment_factor': ['emission', 'innovation', 'resource'],
            'social_factor': ['human_rights', 'product_responsibility', 'workforce', 'community'],
            'governance_factor': ['management', 'shareholders', 'csr_strategy'],
        }

        # Initialize factors as dictionaries
        factor_values = {factor: 0 for factor in factors.keys()}

        # Calculate the sum of values
        total_value = 0
        for factor, attribute_list in factors.items():
            for attr in attribute_list:
                value = getattr(self, attr, 0)
                if value is not None:
                    total_value += value

        if total_value == 0:
            # Handle the case where total_value is zero to avoid division by zero
            for factor in factors.keys():
                setattr(self, factor, 0)
        else:
            for factor, attribute_list in factors.items():
                factor_value = sum(getattr(self, attr, 0) for attr in attribute_list if getattr(self, attr) is not None)
                factor_values[factor] = factor_value / total_value

            # Set the calculated factor values in the model instance
            for factor, value in factor_values.items():
                setattr(self, factor, value)

        super(Sector, self).save(*args, **kwargs)