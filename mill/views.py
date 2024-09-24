from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions, viewsets

from rest_framework import mixins

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
        .prefetch_related('productions', 'purchases', 'items__returns')\
        .all()

    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        production_queryset = Production.objects.filter(
            product_id=self.kwargs['pk'])

        purchase_queryset = Purchase.objects.filter(
            product_id=self.kwargs['pk'])

        if production_queryset.count() > 0 or purchase_queryset.count() > 0:
            return Response({'product': 'Product cannot be deleted.'}, status=400)

        return super().destroy(request, *args, **kwargs)


class CustomerViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerialzer

    def destroy(self, request, *args, **kwargs):
        if Command.objects.filter(customer_id=self.kwargs['pk']).count() > 0:
            return Response({'product': 'Customer cannot be deleted.'}, status=400)

        return super().destroy(request, *args, **kwargs)


class ProductionViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    queryset = Production.objects.all()
    serializer_class = ProductionSerializer


class CommandViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Command.objects.prefetch_related('items__returns').all()

    def get_serializer_class(self):
        if self.action == 'update':
            return UpdateCommandSerializer
        return CommandSerializer

    def destroy(self, request, *args, **kwargs):
        if Item.objects.filter(command_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Command cannot be deleted.'}, status=400)
        return super().destroy(request, *args, **kwargs)


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
            .all()

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
        context = super().get_serializer_context()
        context['item_id'] = self.kwargs['item_pk']
        return context

    def get_queryset(self):
        item_id = self.kwargs['item_pk']
        get_object_or_404(Item, pk=item_id)

        return ItemReturn.objects\
            .filter(item_id=item_id)\
            .all()


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
