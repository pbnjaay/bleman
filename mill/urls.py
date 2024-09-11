from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('customers', views.CustomerViewSet, basename='customers')
router.register('commands', views.CommandViewSet, basename='commands')

command_router = routers.NestedDefaultRouter(
    router, 'commands', lookup='command')
command_router.register(
    'items', views.ItemViewSet, basename='command-items')

item_router = routers.NestedDefaultRouter(
    command_router, 'items', lookup='item')
item_router.register('returns', views.ItemReturnViewSet,
                     basename='item-returns')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(command_router.urls)),
    path('', include(item_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
