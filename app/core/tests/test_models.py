from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@defynance.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating  a new user with an email is successful"""
        email = 'test@london.com'
        password = 'Test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
            )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@LONDON.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_superuser(self):
        """Test Creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@defynance.com',
            'test123'
            )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Test'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
            )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='steak and mushroom sauce',
            time_minutes=5,
            price=5.00
            )

        self.assertEqual(str(recipe), recipe.title)

    def test_growthratebyageeducation_str(self):
        """Test growth rate by age and education str"""
        growth_rate = models.GrowthRateByAgeEducation.objects.create(
            age=23,
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

        self.assertEqual(str(growth_rate), str(growth_rate.age))

    def test_pricing_str(self):
        """Test pricing string representation"""
        pricing = models.Pricing.objects.create(
            term=10,
            interest_rate=0.1,
            min_cagr=0.1,
            targeted_cagr=0.1,
            max_cagr=0.1,
            payment_cap_factor=0.1,
            prepayment_fv=0.1,
            prepayment_growth=0.1
        )
        self.assertEqual(str(pricing), str(pricing.term))

    def test_unmeploymentbyindustry(self):
        """Test unemployemnt by industry string representation"""
        unemployment_by_industry = models.UnemploymentByIndustry.objects.create(
            industry_id=0,
            industry="xyz",
            mean_duration=12.1,
            median_duration=25.0
        )

        self.assertEqual(str(unemployment_by_industry),unemployment_by_industry.industry)

    def test_unemployment_by_occupation(self):
        """Test unemployment by occupation string represenation"""
        unemployment_by_occupation = models.UnemploymentByOccupation.objects.create(
            occupation_id=0,
            occupation='xyz',
            occupation_type='asd',
            mean_duration=12.0,
            median_duration=6.5

        )

        self.assertEqual(str(unemployment_by_occupation), unemployment_by_occupation.occupation)

    def test_unemployment_by_age_group(self):
        """Test unemployment by agegroup string represenation"""
        unemployment_by_agegroup = models.UnemploymentByAgeGroup.objects.create(
            age_group='20-23',
            age_min=20,
            age_max=23,
            mean_duration=12.4,
            median_duration=6.5
        )

        self.assertEqual(str(unemployment_by_agegroup),unemployment_by_agegroup.age_group)

    def test_employment_duration_by_agegroup(self):
        """Test employment duration by age group"""
        employment_duratiom_agegroup = models.EmploymentDurationByAgeGroup.objects.create(
            updated_date="2020-02-02",
            age_group="20-23",
            age_min=20,
            age_max=23,
            duration=36
        )

        self.assertEqual(str(employment_duratiom_agegroup),employment_duratiom_agegroup.age_group)
