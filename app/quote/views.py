from rest_framework.views import APIView
from rest_framework import viewsets, mixins,generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from core.models import GrowthRateByAgeEducation, UnemploymentByAgeGroup,\
                        UnemploymentByIndustry,UnemploymentByOccupation,\
                        Pricing,EmploymentDurationByAgeGroup
from quote import serializers
from quote.quote import Prais
import json

class QuoteViewSet(APIView):
    """ Process quotes"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    # serializer_class = serializers.QuoteSerializer
    def get_queryset(self):
        pass

    def get(self, request, *args, **kwargs):
        """
        Quotes request should have following parameters
        funding_amount,current_income,age,degree,industry(optional),
        profession(optional),method(optional),term_list(optional in years)
        """
        term_flag = 0
        paras = request.query_params
        funding_amount = float(paras['funding_amount'])
        current_income = float(paras['current_income'])
        age = int(paras['age'])
        degree = paras['degree']

        if 'industry'in paras.keys():
            industry = request.query_params['industry']

        if 'profession' in paras.keys():
            profession = request.query_params['profession']

        if 'method' in paras.keys():
            method = request.query_params['method']

        if 'term_list' in paras.keys():
            term_list = eval(request.query_params['term_list'])
            term_flag = 1
            print('here')

        prais = Prais()
        if term_flag == 1:
            quotes_result = prais.Quotes(funding_amount,current_income,age,degree,term_list=term_list)
        else :
            quotes_result = prais.Quotes(funding_amount,current_income,age,degree)

        quotes_json = quotes_result#json.dumps(quotes_result)
        # except:
        #     return Response(status.HTTP_406_NOT_ACCEPTABLE)
        return Response(quotes_json)
