from rest_framework import serializers


from core.models import GrowthRateByAgeEducation, UnemploymentByAgeGroup,\
                        UnemploymentByIndustry,UnemploymentByOccupation,\
                        Pricing,EmploymentDurationByAgeGroup


class GrowthRateByAgeEducationSerializer(serializers.Serializer):
    """Serializer for tag objects"""

    class Meta:
        model = GrowthRateByAgeEducation
        fields = ('age')
        read_only_fields = ('age', )

# class QuoteSerializer(serializers.ModelSerializer):
#     """Serializer for quote generator"""
#
#     class Meta:
#         model =
#
# class GrowthRateByAgeEducationSerializer(serializers.ModelSerializer):
#     """Serializer a Growth Rate By A"""
#     ingredients = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Ingredient.objects.all()
#     )
#     tags = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Tag.objects.all()
#     )
#
#     class Meta:
#         model = Recipe
#         fields = (
#             'id', 'title', 'ingredients', 'tags', 'time_minutes', 'price',
#             'link',
#             )
#         read_only_fields = ('id', )
