from django.urls import path
from rest_framework.routers import DefaultRouter

from products import views


app_name = 'products'
router = DefaultRouter()
router.include_root_view = False
router.register('', views.ProductView, basename='product')

urlpatterns = [
    path('categories/', views.CategoriesTreeView.as_view(), name='categories-list'),
    *router.urls,
]
