from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from mill.models import (Command, Customer, Item, ItemReturn, Product,
                         Production, Purchase)
from mill.pagination import PageNumberPagination
from mill.serializers import (AddItemSerializer, CommandSerializer,
                              CustomerSerialzer, ItemReturnSerializer,
                              ItemSerializer, ProductionSerializer,
                              ProductSerializer, PurchaseSerializer,
                              UpdateCommandSerializer, UpdateItemSerializer)


class ProductViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Product.objects\
        .get_product_with_quantity_in_stock()\
        .order_by('name')\
        .prefetch_related(
            'productions',
            'purchases',
            'items__returns'
        )

    serializer_class = ProductSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Customer.objects.order_by('surname').all()
    serializer_class = CustomerSerialzer


class ProductionViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    queryset = Production.objects.order_by('production_date').all()
    serializer_class = ProductionSerializer


class CommandViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Command.objects.prefetch_related('items__returns').order_by('-id')

    def get_serializer_class(self):
        if self.action == 'update':
            return UpdateCommandSerializer
        return CommandSerializer


class ItemViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        get_object_or_404(Command, id=self.kwargs.get('command_pk'))
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        command_id = self.kwargs.get('command_pk')

        return Item.objects\
            .filter(command_id=command_id)\
            .select_related('product')\
            .prefetch_related('returns')\
            .order_by('-id')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['command_id'] = self.kwargs.get('command_pk')
        return context

    def get_serializer_class(self):
        if self.action == 'create':
            return AddItemSerializer
        if self.action == 'partial_update':
            return UpdateItemSerializer
        return ItemSerializer


class ItemReturnViewSet(viewsets.ModelViewSet):
    serializer_class = ItemReturnSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'item_id': self.kwargs['item_pk']}

    def get_queryset(self):
        item_id = self.kwargs['item_pk']
        get_object_or_404(Item, pk=item_id)

        return ItemReturn.objects\
            .order_by('-id')\
            .filter(item_id=item_id)


class PurchaseViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class ProductionViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = ProductionSerializer
    queryset = Production.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
