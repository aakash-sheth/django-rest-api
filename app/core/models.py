from django.db import models
from django.contrib.auth.models import AbstractBaseUser,\
                        BaseUserManager, PermissionsMixin
from django.conf import settings

# Create your models here


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and save a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that support using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be usd in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )

    def __str__(self):
        return self.name


class Recipe(models.Model):
        """Recipe object"""
        user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE
        )
        title = models.CharField(max_length=255)
        time_minutes = models.IntegerField()
        price = models.DecimalField(max_digits=5, decimal_places=2)
        link = models.CharField(max_length=255, blank=True)
        ingredients = models.ManyToManyField('Ingredient')
        tags = models.ManyToManyField('Tag')

        def __str__(self):
            return self.title


class GrowthRateByAgeEducation(models.Model):
    """Growth Rate Table by Age and Education"""
    updated_date = models.DateField(auto_now=True)
    age = models.IntegerField(unique=True)
    dropout = models.DecimalField(max_digits=6, decimal_places=3)
    diploma = models.DecimalField(max_digits=6, decimal_places=3)
    some_college = models.DecimalField(max_digits=6, decimal_places=3)
    associates = models.DecimalField(max_digits=6, decimal_places=3)
    license = models.DecimalField(max_digits=6, decimal_places=3)
    bachelors = models.DecimalField(max_digits=6, decimal_places=3)
    masters = models.DecimalField(max_digits=6, decimal_places=3)
    mba = models.DecimalField(max_digits=6, decimal_places=3)
    attorney = models.DecimalField(max_digits=6, decimal_places=3)
    doctorate = models.DecimalField(max_digits=6, decimal_places=3)
    professional = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return str(self.age)


class Pricing(models.Model):
    """Table for ISA pricing"""
    updated_date = models.DateField(auto_now=True)
    term = models.IntegerField(unique=True)
    interest_rate = models.DecimalField(max_digits=6, decimal_places=4)
    min_cagr = models.DecimalField(max_digits=5, decimal_places=3)
    targeted_cagr = models.DecimalField(max_digits=5, decimal_places=3)
    max_cagr = models.DecimalField(max_digits=5, decimal_places=3)
    payment_cap_factor = models.DecimalField(max_digits=5, decimal_places=3)
    prepayment_fv = models.DecimalField(max_digits=5, decimal_places=3)
    prepayment_growth = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return str(self.term)


class UnemploymentByIndustry(models.Model):
    """Table of Mean and Median Unemployment Duration in Weeks by Industry (NAICS) """
    updated_date = models.DateField(auto_now=True)
    industry_id = models.IntegerField()
    industry = models.CharField(max_length=255)
    mean_duration = models.DecimalField(max_digits=4, decimal_places=1)
    median_duration = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return self.industry


class UnemploymentByOccupation(models.Model):
    """Table of Mean and Median Unemployment Duration in Weeks by Occupation (NAICS) """
    updated_date = models.DateField(auto_now=True)
    occupation_id = models.IntegerField()
    occupation = models.CharField(max_length=255)
    occupation_type = models.CharField(max_length=255)
    mean_duration = models.DecimalField(max_digits=4, decimal_places=1)
    median_duration = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return self.occupation


class UnemploymentByAgeGroup(models.Model):
    """Table of Mean and Median Unemployment Duration in Weeks by Age Group """
    updated_date = models.DateField(auto_now=True)
    age_group = models.CharField(max_length=255)
    age_min = models.IntegerField()
    age_max = models.IntegerField()
    mean_duration = models.DecimalField(max_digits=4, decimal_places=1)
    median_duration = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return self.age_group


class EmploymentDurationByAgeGroup(models.Model):
    """Table of Mean and Median Employment Duration in Months by Age Group """
    updated_date = models.DateField(auto_now=True)
    age_group = models.CharField(max_length=255)
    age_min = models.IntegerField()
    age_max = models.IntegerField()
    duration = models.DecimalField(max_digits=4, decimal_places=1)


    def __str__(self):
        return self.age_group


class HikesByEducation(models.Model):
    """Table of average % hike by Education based on what farrukh(asshole) thinks"""
    updated_date = models.DateField(auto_now=True)
    degree = models.CharField(max_length=255)
    hike = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return str(self.degree)

#
# class Quote(models.Model):
#     """Quotes Calculated"""
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL
#     )
#     customer_id = models.CharField(ma)
