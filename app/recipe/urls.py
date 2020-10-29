from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

# DefualtRouter automatically create register different urls
# associated with different elements of the app e.g. /app/tags , /app/tags/1

router = DefaultRouter()
router.register('ingredients', views.IngredientViewSet)
router.register('tags', views.TagViewSet)
router.register('recipe', views.RecipeViewSet)
# router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
