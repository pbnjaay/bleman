from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from mill.models import (Command, Customer, Item, ItemReturn, Product,
                         Production)
from mill.pagination import PageNumberPagination
from mill.serializers import (AddItemSerializer, CommandSerializer,
                              CustomerSerialzer, ItemReturnSerializer,
                              ItemSerializer, ProductionSerializer,
                              ProductSerializer, UpdateCommandSerializer,
                              UpdateItemSerializer)


class ProductViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Product.objects\
        .annotate(
            quantity_in_stock=(
                Coalesce(Sum('purchases__quantity'), Value(0)) +
                Coalesce(Sum('productions__quantity'), Value(0)) -
                Coalesce(Sum('items__quantity'), Value(0)) +
                Coalesce(Sum('items__returns__quantity'), Value(0))
            )
        ).order_by('name')\
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
