from rest_framework import viewsets, mixins,generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from core.models import GrowthRateByAgeEducation, UnemploymentByAgeGroup,\
                        UnemploymentByIndustry,UnemploymentByOccupation,\
                        Pricing,EmploymentDurationByAgeGroup
from quote import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    """Manage viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new ingredient"""
        serializer.save(user=self.request.user)

class QuoteViewSet(BaseRecipeAttrViewSet):
    """ Manage Quote History in the database"""
    queryset = GrowthRateByAgeEducation.objects.all()
    # serializer_class = serializers.QuoteSerializer

class GetGrowthRateView(BaseRecipeAttrViewSet):
    """ Manage Quote History in the database"""
    queryset = GrowthRateByAgeEducation.objects.all()
    # serializer_class = serializers.QuoteSerializer
