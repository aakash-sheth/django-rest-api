from rest_framework.views import APIView
from rest_framework import viewsets, mixins,generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from core.models import GrowthRateByAgeEducation, UnemploymentByAgeGroup,\
                        UnemploymentByIndustry,UnemploymentByOccupation,\
                        Pricing,EmploymentDurationByAgeGroup
from quote import serializers
from quote.quote import Prais
import json


# @api_view
# @permissions_classes([AllowAny])



# @api_view()
# @permission_classes([AllowAny])
# def QuoteView(request):
#   funding_amount = request.query_params
#   print(funding_amount)
#   print('here')
#   return Response({'Message':"We recieved your request."})

class QuoteViewSet(APIView):
    """ Process quotes"""

    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, )
    # # serializer_class = serializers.QuoteSerializer
    # def get_queryset(self):
    #     pass

    def get(self, request, *args, **kwargs):
        """
        Quotes request should have following parameters
        funding_amount,current_income,age,degree,industry(optional),
        profession(optional),method(optional),term_list(optional in years)
        """
        funding_amount = float(request.query_params['funding_amount'])
        current_income = float(request.query_params['current_income'])
        age = int(request.query_params['age'])
        degree = request.query_params['degree']
        # industry = request.query_params['industry']
        # profession = request.query_params['profession']
        # method = request.query_params['method']
        # term_list = request.query_params['term_list']
        print(degree)
        prais = Prais()
        quotes_result = prais.Quotes(funding_amount,current_income,age,degree)
        quotes_json = json.dumps(quotes_result)
        # except:
        #     return Response(status.HTTP_406_NOT_ACCEPTABLE)
        return Response(quotes_json)
# class BaseAttrViewSet(viewsets.GenericViewSet,
#                     mixins.ListModelMixin,
#                     mixins.CreateModelMixin):
#     """Manage viewset for user owned recipe attributes"""
#     authentication_classes = (TokenAuthentication, )
#     permission_classes = (IsAuthenticated, )
#     def get_queryset(self):
#         """Return objects for the current authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')
#
#     def perform_create(self, serializer):
#         """Create a new ingredient"""
#         serializer.save(user=self.request.user)
#
# class QuoteViewSet(BaseRecipeAttrViewSet):
#     """ Manage Quote History in the database"""
#     serializer_class = serializers.RecipeSerializer
#
#     authentication_classes = (TokenAuthentication, )
#     permission_classes = (IsAuthenticated, )
#     # serializer_class = serializers.QuoteSerializer
