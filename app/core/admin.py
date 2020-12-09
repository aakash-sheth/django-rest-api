from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
# this is require for the translations engine in multiple languages
from core import models


class UserAdmin(BaseUserAdmin):

    ordering = ['id']
    list_display = ['email', 'name']
# each bracket in the fieldset is a section
    fieldsets = (
                (None, {'fields': ('email', 'password')}),
                (_('Personal Info'), {'fields': ('name', )}),
                (
                    _('Permissions'),
                    {'fields': ('is_active', 'is_staff', 'is_superuser')}
                ),
                (_('Important dates'), {'fields': ('last_login', )})
                )

    add_fieldsets = (
                    (None, {
                        'classes': ('wide', ),
                        'fields': ('email', 'password1', 'password2')

                    }),
                    )


# Register your models here.
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
admin.site.register(models.GrowthRateByAgeEducation)
admin.site.register(models.UnemploymentByIndustry)
admin.site.register(models.UnemploymentByOccupation)
admin.site.register(models.UnemploymentByAgeGroup)
admin.site.register(models.Pricing)
admin.site.register(models.EmploymentDurationByAgeGroup)
admin.site.register(models.HikesByEducation)
# admin.site.register(models.Pricing
