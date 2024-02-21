from rest_framework import serializers
from .models import Sector,CompanyDetails
from rest_framework import serializers

from rest_framework import serializers
from api.models import EsgScore

class EsgScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = EsgScore
        fields = [
            'polarity_score', 'environment_score', 'social_score', 'governance_score',
            'emission', 'innovation', 'resource', 'human_rights', 'product_responsibility',
            'workforce', 'community', 'management', 'shareholders', 'csr_strategy',
        ]



class CompanySymbolSerializer(serializers.Serializer):
    description = serializers.CharField()
    displaySymbol = serializers.CharField()
    symbol = serializers.CharField()
    type = serializers.CharField()



class CompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = '__all__'



class CompanySectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'


class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = ['company_name']