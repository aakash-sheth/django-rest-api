from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from django.db.models import Q
from rest_framework import status
from rest_framework.test import APIClient
from quote.quote import Prais
from core.models import GrowthRateByAgeEducation, UnemploymentByAgeGroup,\
                        UnemploymentByIndustry,UnemploymentByOccupation,\
                        Pricing,EmploymentDurationByAgeGroup, User,\
                        PraisParameterCap, HikesByEducation
from quote import views
QUOTE_URL = reverse('quote:quotes')

# class PublicQuoteApiTests(TestCase):
#     """Test the publically available quotes API"""
#
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_login_required(self):
#         """Test that login is required to access this endpoint"""
#         res = self.client.get(QUOTE_URL)
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateQuoteApiTests(TestCase):
    """Test quotes can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_praisparas(self):
        """Test that GetPraisFixedPara functions returns latest isa parameters"""

        isa_para = PraisParameterCap.objects.create(
                    isa_processing_fee=0.2 ,
                    isa_servicing_fee=0.02,
                    isa_sales_charge=1.2,
                    minimum_self_equity_perc=0.05,
                    max_minimum_self_equity=12,
                    annual_lower_income=12,
                    isa_processing_fee_cap=111,
                    buyout_servicing_fee=0.07,
                    isp_age_factor=0.25)

        prais = Prais()
        latest_para = prais.GetPraisFixedPara()

        self.assertEqual(1.2, float(latest_para.isa_sales_charge))

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
        unemp_start,unemp_months= prais.GetUnemploymentLists(age=27,
                        term=5,method="Median",industry="NA",profession="NA")
        self.assertEqual([37], unemp_start)
        self.assertEqual([3],unemp_months)

    def test_GetQuote(self):
        """Test GetQuote function returns a right output"""

        isa_para = PraisParameterCap.objects.create(
                    isa_processing_fee=0.01 ,
                    isa_servicing_fee=0.05,
                    isa_sales_charge=0.02,
                    minimum_self_equity_perc=0.05,
                    max_minimum_self_equity=5000,
                    annual_lower_income=25000,
                    isa_processing_fee_cap=1500,
                    buyout_servicing_fee=0.05,
                    isp_age_factor=2.5)

        prais= Prais()
        Quote = prais.GetQuote(funding_amount=31000,
                                current_income=44000,
                                growth_rate=0.03 ,
                                unemployment_start_list=[37],
                                term=5,
                                age=26,
                                hike=0.03,
                                unemployment_months_list=[3],
                                targeted_return=0.03)
        self.assertEqual(5,Quote['term'])

    def test_GetQuote(self):
        """Test GetQuote function returns a right output"""

        isa_para = PraisParameterCap.objects.create(
                    isa_processing_fee=0.01 ,
                    isa_servicing_fee=0.05,
                    isa_sales_charge=0.02,
                    minimum_self_equity_perc=0.05,
                    max_minimum_self_equity=5000,
                    annual_lower_income=25000,
                    isa_processing_fee_cap=1500,
                    buyout_servicing_fee=0.05,
                    isp_age_factor=2.5)

        growth_rate = GrowthRateByAgeEducation.objects.create(
                                                    age=26,
                                                    dropout=0.03,
                                                    diploma=0.03,
                                                    some_college=0.03,
                                                    associates=0.03,
                                                    license=0.03,
                                                    bachelors=0.03,
                                                    masters=0.03,
                                                    mba=0.03,
                                                    attorney=0.03,
                                                    doctorate=0.03,
                                                    professional=0.03,
                                                )
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

        hike_by_education = HikesByEducation.objects.create(
            updated_date="2020-02-02",
            degree="masters",
            hike=0.03,
        )

        pricing = Pricing.objects.create(
            term=7,
            interest_rate=0.1,
            min_cagr=0.1,
            targeted_cagr=0.0325,
            max_cagr=0.1,
            payment_cap_factor=0.1,
            prepayment_fv=0.1,
            prepayment_growth=0.1
        )

        prais= Prais()

        Quote = prais.Quotes(funding_amount=31000,
                              current_income=44000,
                              age=26,
                              degree='masters',
                              industry="NA",
                              profession="NA",
                              method="Median",
                              term_list = [7])
        print(Quote)
        self.assertEqual(7,Quote[7]['term'])

    def test_quoteurl(self):
        """Test that quote url api returns the right output"""
        isa_para = PraisParameterCap.objects.create(
                    isa_processing_fee=0.01 ,
                    isa_servicing_fee=0.05,
                    isa_sales_charge=0.02,
                    minimum_self_equity_perc=0.05,
                    max_minimum_self_equity=5000,
                    annual_lower_income=25000,
                    isa_processing_fee_cap=1500,
                    buyout_servicing_fee=0.05,
                    isp_age_factor=2.5)

        growth_rate = GrowthRateByAgeEducation.objects.create(
                                                    age=26,
                                                    dropout=0.03,
                                                    diploma=0.03,
                                                    some_college=0.03,
                                                    associates=0.03,
                                                    license=0.03,
                                                    bachelors=0.03,
                                                    masters=0.03,
                                                    mba=0.03,
                                                    attorney=0.03,
                                                    doctorate=0.03,
                                                    professional=0.03,
                                                )
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

        hike_by_education = HikesByEducation.objects.create(
            updated_date="2020-02-02",
            degree="masters",
            hike=0.03,
        )

        pricing = Pricing.objects.create(
            term=7,
            interest_rate=0.1,
            min_cagr=0.1,
            targeted_cagr=0.0325,
            max_cagr=0.1,
            payment_cap_factor=0.1,
            prepayment_fv=0.1,
            prepayment_growth=0.1
        )

        payload = {
        'funding_amount': 31000,
        'current_income': 44000,
        'age': 26,
        'degree': 'masters',
        'term_list':[7]
        }

        res = self.client.get(QUOTE_URL, payload)
