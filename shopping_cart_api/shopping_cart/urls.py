from rest_framework.routers import DefaultRouter

from shopping_cart import views


app_name = 'shopping_cart'
router = DefaultRouter()
router.include_root_view = False
router.register('', views.ShoppingCartView, basename='cart')
router.register('orders', views.UserOrdersView, basename='orders')

urlpatterns = [
    *router.urls,
]
