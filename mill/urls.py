from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('customers', views.CustomerViewSet, basename='customers')
router.register('purchases', views.PurchaseViewSet, basename='purchases')
router.register('productions', views.ProductionViewSet, basename='productions')
router.register('orders', views.OrderViewSet, basename='orders')

order_router = routers.NestedDefaultRouter(
    router, 'orders', lookup='order')
order_router.register(
    'items', views.ItemViewSet, basename='order-items')

order_router.register('payments', views.PaymentViewSet,
                      basename='order-payments')

item_router = routers.NestedDefaultRouter(
    order_router, 'items', lookup='item')
item_router.register('returns', views.ItemReturnViewSet,
                     basename='item-returns')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(order_router.urls)),
    path('', include(item_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
