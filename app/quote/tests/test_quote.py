from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from django.db.models import Q
from rest_framework import status
from rest_framework.test import APIClient
from quote.quote import Prais
from core.models import GrowthRateByAgeEducation, UnemploymentByAgeGroup,\
                        UnemploymentByIndustry,UnemploymentByOccupation,\
                        Pricing,EmploymentDurationByAgeGroup, User
QUOTE_URL = reverse('quote:growthrate')
#
# class PublicQuoteApiTests(TestCase):
#     """Test the publically available ingredients API"""
#
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_login_required(self):
#         """Test that login is required to access this endpoint"""
#         res = self.client.get(QUOTE_URL)
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateQuoteApiTests(TestCase):
    """Test ingredients can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_getgrowthrate(self):
        """Test that GetGrowthRate functions returns the right growth rate"""
        growth_rate = GrowthRateByAgeEducation.objects.create(
            age=100,
            dropout=2.0,
            diploma=2.0,
            some_college=2.0,
            associates=0.02,
            license=2.0,
            bachelors=2.0,
            masters=2.0,
            mba=2.0,
            attorney=2.0,
            doctorate=2.0,
            professional=2.0,
        )

        prais= Prais()
        growth_rate = prais.GetGrowthRate(age=100,
                                            degree='masters',
                                            profession='NA',
                                            industry='NA')

        self.assertEqual(2, growth_rate)

    def test_getgrowthrateforwrongdegree(self):
        """Test GetGrowthRate function returns 'NA' for wrong degree"""
        growth_rate = GrowthRateByAgeEducation.objects.create(
            age=100,
            dropout=2.0,
            diploma=2.0,
            some_college=2.0,
            associates=0.02,
            license=2.0,
            bachelors=2.0,
            masters=2.0,
            mba=2.0,
            attorney=2.0,
            doctorate=2.0,
            professional=2.0,
        )
        prais= Prais()
        growth_rate = prais.GetGrowthRate(age=100,
                                            degree='master',
                                            profession='NA',
                                            industry='NA')

        self.assertEqual("NA", growth_rate)


    def test_getgrowthrateforwrongage(self):
        """Test GetGrowthRate functions returns 'NA' if entered age is wrong"""
        growth_rate = GrowthRateByAgeEducation.objects.create(
            age=100,
            dropout=2.0,
            diploma=2.0,
            some_college=2.0,
            associates=0.02,
            license=2.0,
            bachelors=2.0,
            masters=2.0,
            mba=2.0,
            attorney=2.0,
            doctorate=2.0,
            professional=2.0,
        )
        prais= Prais()
        growth_rate = prais.GetGrowthRate(age=101,
                                            degree='masters',
                                            profession='NA',
                                            industry='NA')

        self.assertEqual("NA", growth_rate)

    def test_GetEmploymentDuration(self):
        """Test GetEmploymentDuration function returns the right employment
        duration in years"""
        employment_duratiom_agegroup = EmploymentDurationByAgeGroup.objects.create(
            age_group="25-34",
            age_min=25,
            age_max=34,
            duration=2.8
        )
        prais= Prais()
        employment_duration = prais.GetEmploymentDuration(age=27)

        self.assertEqual(2.8,employment_duration)

    def test_GetEmploymentDuration(self):
        """Test GetEmploymentDuration function returns the right employment
        duration in years"""
        unemployment_duration_agegroup = UnemploymentByAgeGroup.objects.create(
                                                        age_group='25-34',
                                                        age_min=25,
                                                        age_max=34,
                                                        mean_duration=23.0,
                                                        median_duration=10.0
                                                    )
        prais= Prais()
        employment_duration = prais.GetUemploymentByAgeGroup(age=27,
                                                            method="Median")

        self.assertEqual(10.0,employment_duration)

    def test_GetUnemploymentLists(self):
        """Test GetUnemploymentLists functions returns a right list"""

        unemployment_duration_by_agegroup = UnemploymentByAgeGroup.objects.create(
            age_group="25-34",
            age_min=25,
            age_max=34,
            mean_duration=23.0,
            median_duration=10.0
        )
        employment_duratiom_agegroup = EmploymentDurationByAgeGroup.objects.create(
            age_group="25-34",
            age_min=25,
            age_max=34,
            duration=2.8
        )

        prais= Prais()
        unemp_start,unemp_months,term = prais.GetUnemploymentLists(age=27,
                        term=5,method="Median",industry="NA",profession="NA")
        self.assertEqual([37], unemp_start)
        self.assertEqual([3],unemp_months)
        self.assertEqual(63,term)