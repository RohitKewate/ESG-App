import requests
import json
import scrapydo
from decimal import Decimal
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import numpy as np
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import urllib.parse
from django.shortcuts import  get_object_or_404
from django.db.models import Q
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from rest_framework.response import Response
from .serializers import CompanySectorSerializer,CompanyDetailsSerializer,CompanySymbolSerializer, CompanyNameSerializer,EsgScoreSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.utils.http import urlencode
from .models import Sector,CompanyDetails,EsgScore
import finnhub
from scraper.scraper.spiders.spider import EmissionSpider,InnovationSpider,ResourceSpider,HumanSpider,ProductSpider,WorkforceSpider,CommunitySpider,ManagementSpider,ShareholderSpider,CsrStrategySpider
import environ
import os
from dotenv import load_dotenv
from .tasks import run_spider


load_dotenv('.env.local')
finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

#API's for utility

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_company_symbol(request):
    query = request.query_params.get('q')

    data = finnhub_client.symbol_lookup(query)

    if "result" in data:
        results = data["result"]
        count = len(results)
    else:
        results = []
        count = 0

    # Serialize the results
    serializer = CompanySymbolSerializer(results, many=True)
    
    # Create the response data with count and results
    response_data = {
        "count": count,
        "result": serializer.data,
    }
    
    return Response(response_data)



@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_company_details(request):
    symbol = request.query_params.get('symbol')
    
    data = finnhub_client.company_profile2(symbol=symbol)
    
    # Check if the sector already exists, or create it if it doesn't
    sector, created = Sector.objects.get_or_create(sector=data["finnhubIndustry"])
    
    # Create or update CompanyDetails using the existing or newly created sector
    company, created = CompanyDetails.objects.get_or_create(
        company_name=data["name"],
        symbol=data["ticker"],
        url=urllib.parse.quote(data["weburl"]),
        sector=sector,  # Use the saved or existing sector object
        logo = data["logo"]
    )
    print(f"Company Details Object: {company}")
    print(f"Company Name: {company.company_name}")
    print(f"Symbol: {company.symbol}")


    # Serialize the CompanyDetails object using the correct serializer class
    serializer = CompanyDetailsSerializer(company,many=False)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_company_esg_sector(request):
    id = request.query_params.get('id')
    sector_data = Sector.objects.filter(id=id)[0]
    serializer = CompanySectorSerializer(sector_data,many=False)
    print(os.getenv("FINNHUB_API_KEY"))
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_company_name_for_spider(request):
    company_name = request.query_params.get('q')
    company_name_data = CompanyDetails.objects.filter(Q(company_name__icontains=company_name) )[0]
    serializer = CompanyNameSerializer(company_name_data,many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_esg_score(request):
    symbol = request.GET.get('symbol', None)
    
    if symbol is None:
        return JsonResponse({'error': 'Missing company symbol'}, status=400)

    try:
        company = get_object_or_404(CompanyDetails, symbol=symbol)
        esg_score = EsgScore.objects.get(company=company)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    serializer = EsgScoreSerializer(esg_score)
    return JsonResponse(serializer.data)


#API's for ESG factors

from .serializers import EsgScoreSerializer  # adjust the import based on your project structure
from api.models import CompanyDetails  # import the CompanyDetails model

scrapydo.setup()

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def emmision_spider(request):
    try:
        company_name = request.query_params.get('q', None)
        if company_name is None:
            return Response({'error': 'Company name not provided'}, status=400)

        response = requests.get(f'{os.getenv("BASE_URL")}/api/spider?q={company_name}')
        if response.status_code != 200:
            return Response({'error': f"Error getting company name: {response.text}"}, status=400)

        company_name = response.json()['company_name']
        results = scrapydo.run_spider(EmissionSpider, company_name=company_name)
        print(f"Spider returned {len(results)} results")
        if not results:
            return Response({'error': 'No articles found for analysis'}, status=404)

        # Check if all articles have no text
        if all('score' not in item for item in results):
            return Response({'error': 'No text in articles to analyze'}, status=404)

        log_scores = np.log([item['score'] for item in results if 'score' in item])
        if len(log_scores) == 0:
            return Response({'error': 'No scores to calculate average score'}, status=404)

        average_score = np.exp(np.mean(log_scores))
        # Convert average_score to a Decimal
        average_score = Decimal(str(average_score))

        # Retrieve the CompanyDetails instance
        company = CompanyDetails.objects.get(company_name=company_name)
      
        emission, create = EsgScore.objects.update_or_create(company=company, defaults={'emission':average_score})

        serializer = EsgScoreSerializer(emission)
        return Response({'message': 'Spider run successfully', 'emission': serializer.data})

    except CompanyDetails.DoesNotExist:  # handle the case where the company does not exist
        return Response({'error': f"Company {company_name} does not exist"}, status=404)
    except Exception as e:
        return Response({'error': f"Unexpected error: {str(e)}"}, status=500)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def innovation_spider(request):
    try:
        company_name = request.query_params.get('q', None)
        if company_name is None:
            return Response({'error': 'Company name not provided'}, status=400)

        response = requests.get(f'{os.getenv("BASE_URL")}/api/spider?q={company_name}')
        if response.status_code != 200:
            return Response({'error': f"Error getting company name: {response.text}"}, status=400)

        company_name = response.json()['company_name']
        results = scrapydo.run_spider(InnovationSpider, company_name=company_name)
        if not results:
            return Response({'error': 'Nothing to analyse'}, status=404)

        # Retrieve the CompanyDetails instance
        company = CompanyDetails.objects.get(company_name=company_name)
        
        average_score = sum(item['score'] for item in results) / len(results)
        # Convert average_score to a Decimal
        average_score = Decimal(str(average_score))
        innovation, create = EsgScore.objects.update_or_create(company=company, defaults={'innovation':average_score})

        serializer = EsgScoreSerializer(innovation)
        return Response({'message': 'Spider run successfully', 'innovation': serializer.data})

    except ZeroDivisionError:
        return Response({'error': 'No results to calculate average score'}, status=404)
    except CompanyDetails.DoesNotExist:  # handle the case where the company does not exist
        return Response({'error': f"Company {company_name} does not exist"}, status=404)
    except Exception as e:
        return Response({'error': f"Unexpected error: {str(e)}"}, status=500)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def resource_spider(request):
    try:
        company_name = request.query_params.get('q', None)
        if company_name is None:
            return Response({'error': 'Company name not provided'}, status=400)

        response = requests.get(f'{os.getenv("BASE_URL")}/api/spider?q={company_name}')
        if response.status_code != 200:
            return Response({'error': f"Error getting company name: {response.text}"}, status=400)

        company_name = response.json()['company_name']
        results = scrapydo.run_spider(ResourceSpider, company_name=company_name)
        if not results:
            return Response({'error': 'Nothing to analyse'}, status=404)

        # Retrieve the CompanyDetails instance
        company = CompanyDetails.objects.get(company_name=company_name)
        
        average_score = sum(item['score'] for item in results) / len(results)
        # Convert average_score to a Decimal
        average_score = Decimal(str(average_score))
        resource, create = EsgScore.objects.update_or_create(company=company, defaults={'resource':average_score})

        serializer = EsgScoreSerializer(resource)
        return Response({'message': 'Spider run successfully', 'Resource use': serializer.data})

    except ZeroDivisionError:
        return Response({'error': 'No results to calculate average score'}, status=404)
    except CompanyDetails.DoesNotExist:  # handle the case where the company does not exist
        return Response({'error': f"Company {company_name} does not exist"}, status=404)
    except Exception as e:
        return Response({'error': f"Unexpected error: {str(e)}"}, status=500)
    

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def human_spider(request):
    try:
        company_name = request.query_params.get('q', None)
        if company_name is None:
            return Response({'error': 'Company name not provided'}, status=400)

        response = requests.get(f'{os.getenv("BASE_URL")}/api/spider?q={company_name}')
        if response.status_code != 200:
            return Response({'error': f"Error getting company name: {response.text}"}, status=400)

        company_name = response.json()['company_name']
        results = scrapydo.run_spider(HumanSpider, company_name=company_name)
        if not results:
            return Response({'error': 'Nothing to analyse'}, status=404)

        # Retrieve the CompanyDetails instance
        company = CompanyDetails.objects.get(company_name=company_name)
        
        average_score = sum(item['score'] for item in results) / len(results)
        # Convert average_score to a Decimal
        average_score = Decimal(str(average_score))
        factor, create = EsgScore.objects.update_or_create(company=company, defaults={'human_rights':average_score})

        serializer = EsgScoreSerializer(factor)
        return Response({'message': 'Spider run successfully', 'Human Rights': serializer.data})

    except ZeroDivisionError:
        return Response({'error': 'No results to calculate average score'}, status=404)
    except CompanyDetails.DoesNotExist:  # handle the case where the company does not exist
        return Response({'error': f"Company {company_name} does not exist"}, status=404)
    except Exception as e:
        return Response({'error': f"Unexpected error: {str(e)}"}, status=500)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def product_spider(request):
    try:
        company_name = request.query_params.get('q', None)
        if company_name is None:
            return Response({'error': 'Company name not provided'}, status=400)

        response = requests.get(f'{os.getenv("BASE_URL")}/api/spider?q={company_name}')
        if response.status_code != 200:
            return Response({'error': f"Error getting company name: {response.text}"}, status=400)

        company_name = response.json()['company_name']
        results = scrapydo.run_spider(ProductSpider, company_name=company_name)
        if not results:
            return Response({'error': 'Nothing to analyse'}, status=404)

        # Retrieve the CompanyDetails instance
        company = CompanyDetails.objects.get(company_name=company_name)
        
        average_score = sum(item['score'] for item in results) / len(results)
        # Convert average_score to a Decimal
        average_score = Decimal(str(average_score))
        factor, create = EsgScore.objects.update_or_create(company=company, defaults={'product_responsibility':average_score})

        serializer = EsgScoreSerializer(factor)
        return Response({'message': 'Spider run successfully', 'Product Responsibility': serializer.data})

    except ZeroDivisionError:
        return Response({'error': 'No results to calculate average score'}, status=404)
    except CompanyDetails.DoesNotExist:  # handle the case where the company does not exist
        return Response({'error': f"Company {company_name} does not exist"}, status=404)
    except Exception as e:
        return Response({'error': f"Unexpected error: {str(e)}"}, status=500)
    

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def workforce_spider(request):
    try:
        company_name = request.query_params.get('q', None)
        if company_name is None:
            return Response({'error': 'Company name not provided'}, status=400)

        response = requests.get(f'{os.getenv("BASE_URL")}/api/spider?q={company_name}')
        if response.status_code != 200:
            return Response({'error': f"Error getting company name: {response.text}"}, status=400)

        company_name = response.json()['company_name']
        results = scrapydo.run_spider(WorkforceSpider, company_name=company_name)
        if not results:
            return Response({'error': 'Nothing to analyse'}, status=404)

        # Retrieve the CompanyDetails instance
        company = CompanyDetails.objects.get(company_name=company_name)
        
        average_score = sum(item['score'] for item in results) / len(results)
        # Convert average_score to a Decimal
        average_score = Decimal(str(average_score))
        factor, create = EsgScore.objects.update_or_create(company=company, defaults={'workforce':average_score})

        serializer = EsgScoreSerializer(factor)
        return Response({'message': 'Spider run successfully', 'Workforce': serializer.data})

    except ZeroDivisionError:
        return Response({'error': 'No results to calculate average score'}, status=404)
    except CompanyDetails.DoesNotExist:  # handle the case where the company does not exist
        return Response({'error': f"Company {company_name} does not exist"}, status=404)
    except Exception as e:
        return Response({'error': f"Unexpected error: {str(e)}"}, status=500)
    

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def community_spider(request):
    try:
        company_name = request.query_params.get('q', None)
        if company_name is None:
            return Response({'error': 'Company name not provided'}, status=400)

        response = requests.get(f'{os.getenv("BASE_URL")}/api/spider?q={company_name}')
        if response.status_code != 200:
            return Response({'error': f"Error getting company name: {response.text}"}, status=400)

        company_name = response.json()['company_name']
        results = scrapydo.run_spider(CommunitySpider, company_name=company_name)
        if not results:
            return Response({'error': 'Nothing to analyse'}, status=404)

        # Retrieve the CompanyDetails instance
        company = CompanyDetails.objects.get(company_name=company_name)
        
        average_score = sum(item['score'] for item in results) / len(results)
        # Convert average_score to a Decimal
        average_score = Decimal(str(average_score))
        factor, create = EsgScore.objects.update_or_create(company=company, defaults={'community':average_score})

        serializer = EsgScoreSerializer(factor)
        return Response({'message': 'Spider run successfully', 'Community': serializer.data})

    except ZeroDivisionError:
        return Response({'error': 'No results to calculate average score'}, status=404)
    except CompanyDetails.DoesNotExist:  # handle the case where the company does not exist
        return Response({'error': f"Company {company_name} does not exist"}, status=404)
    except Exception as e:
        return Response({'error': f"Unexpected error: {str(e)}"}, status=500)
    

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def management_spider(request):
    try:
        company_name = request.query_params.get('q', None)
        if company_name is None:
            return Response({'error': 'Company name not provided'}, status=400)

        response = requests.get(f'{os.getenv("BASE_URL")}/api/spider?q={company_name}')
        if response.status_code != 200:
            return Response({'error': f"Error getting company name: {response.text}"}, status=400)

        company_name = response.json()['company_name']
        results = scrapydo.run_spider(ManagementSpider, company_name=company_name)
        if not results:
            return Response({'error': 'Nothing to analyse'}, status=404)

        # Retrieve the CompanyDetails instance
        company = CompanyDetails.objects.get(company_name=company_name)
        
        average_score = sum(item['score'] for item in results) / len(results)
        # Convert average_score to a Decimal
        average_score = Decimal(str(average_score))
        factor, create = EsgScore.objects.update_or_create(company=company, defaults={'management':average_score})

        serializer = EsgScoreSerializer(factor)
        return Response({'message': 'Spider run successfully', 'Management': serializer.data})

    except ZeroDivisionError:
        return Response({'error': 'No results to calculate average score'}, status=404)
    except CompanyDetails.DoesNotExist:  # handle the case where the company does not exist
        return Response({'error': f"Company {company_name} does not exist"}, status=404)
    except Exception as e:
        return Response({'error': f"Unexpected error: {str(e)}"}, status=500)
    

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def shareholder_spider(request):
    try:
        company_name = request.query_params.get('q', None)
        if company_name is None:
            return Response({'error': 'Company name not provided'}, status=400)

        response = requests.get(f'{os.getenv("BASE_URL")}/api/spider?q={company_name}')
        if response.status_code != 200:
            return Response({'error': f"Error getting company name: {response.text}"}, status=400)

        company_name = response.json()['company_name']
        results = scrapydo.run_spider(ShareholderSpider, company_name=company_name)
        if not results:
            return Response({'error': 'Nothing to analyse'}, status=404)

        # Retrieve the CompanyDetails instance
        company = CompanyDetails.objects.get(company_name=company_name)
        
        average_score = sum(item['score'] for item in results) / len(results)
        # Convert average_score to a Decimal
        average_score = Decimal(str(average_score))
        factor, create = EsgScore.objects.update_or_create(company=company, defaults={'shareholders':average_score})

        serializer = EsgScoreSerializer(factor)
        return Response({'message': 'Spider run successfully', 'Shareholder': serializer.data})

    except ZeroDivisionError:
        return Response({'error': 'No results to calculate average score'}, status=404)
    except CompanyDetails.DoesNotExist:  # handle the case where the company does not exist
        return Response({'error': f"Company {company_name} does not exist"}, status=404)
    except Exception as e:
        return Response({'error': f"Unexpected error: {str(e)}"}, status=500)
    

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def csr_spider(request):
    try:
        company_name = request.query_params.get('q', None)
        if company_name is None:
            return Response({'error': 'Company name not provided'}, status=400)

        response = requests.get(f'{os.getenv("BASE_URL")}/api/spider?q={company_name}')
        if response.status_code != 200:
            return Response({'error': f"Error getting company name: {response.text}"}, status=400)

        company_name = response.json()['company_name']
        results = scrapydo.run_spider(CsrStrategySpider, company_name=company_name)
        if not results:
            return Response({'error': 'Nothing to analyse'}, status=404)

        # Retrieve the CompanyDetails instance
        company = CompanyDetails.objects.get(company_name=company_name)
        
        average_score = sum(item['score'] for item in results) / len(results)
        # Convert average_score to a Decimal
        average_score = Decimal(str(average_score))
        factor, create = EsgScore.objects.update_or_create(company=company, defaults={'csr_strategy':average_score})

        serializer = EsgScoreSerializer(factor)
        return Response({'message': 'Spider run successfully', 'CSR Strategy': serializer.data})

    except ZeroDivisionError:
        return Response({'error': 'No results to calculate average score'}, status=404)
    except CompanyDetails.DoesNotExist:  # handle the case where the company does not exist
        return Response({'error': f"Company {company_name} does not exist"}, status=404)
    except Exception as e:
        return Response({'error': f"Unexpected error: {str(e)}"}, status=500)
    
    

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def run_task(request):
    try:
        for company in CompanyDetails.objects.all():
            requests.get(f'{os.getenv("BASE_URL")}/api/emission_spider?q={company.company_name}')
            requests.get(f'{os.getenv("BASE_URL")}/api/innovation_spider?q={company.company_name}')
            requests.get(f'{os.getenv("BASE_URL")}/api/resource_spider?q={company.company_name}')
            requests.get(f'{os.getenv("BASE_URL")}/api/human_spider?q={company.company_name}')
            requests.get(f'{os.getenv("BASE_URL")}/api/product_spider?q={company.company_name}')
            requests.get(f'{os.getenv("BASE_URL")}/api/workforce_spider?q={company.company_name}')
            requests.get(f'{os.getenv("BASE_URL")}/api/community_spider?q={company.company_name}')
            requests.get(f'{os.getenv("BASE_URL")}/api/management_spider?q={company.company_name}')
            requests.get(f'{os.getenv("BASE_URL")}/api/shareholder_spider?q={company.company_name}')
            requests.get(f'{os.getenv("BASE_URL")}/api/csr_spider?q={company.company_name}')
            
            print(f"Spider task for {company.company_name} completed successfully") 


    except Exception as e:
        return Response({'error': f"Unexpected error: {str(e)}"}, status=500)

   
    return Response({"message": "Task completed successfully"})

