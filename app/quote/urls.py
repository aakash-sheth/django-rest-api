from django.urls import path, include
from rest_framework.routers import DefaultRouter

from quote import views

# DefualtRouter automatically create register different urls
# associated with different elements of the app e.g. /app/tags , /app/tags/1

router = DefaultRouter()
# router.register('quote', views.QuoteViewSet)
# router.register('ingredients', views.IngredientViewSet)

app_name = 'quote'

urlpatterns = [
    path('', include(router.urls)),
    path('quotes/', views.QuoteViewSet.as_view(), name='quotes')
]
