from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAuthenticatedOrReadOnly , 
    IsAdminUser
)
from drf_yasg.utils import swagger_auto_schema
from .models import Order, User
from . import serializers

User = get_user_model()

# Create your views here.
class HelloOrderView(generics.GenericAPIView):

    @swagger_auto_schema(operation_summary="Hello Order")
    def get(self, request):
        return Response(data={"message":"Hello Order"}, status=status.HTTP_200_OK)


class OrderCreateListView(generics.GenericAPIView):

    serializer_class = serializers.OrderCreationSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Get all Orders")
    def get(self, request):
        orders = Order.objects.all()
        serializer = self.serializer_class(instance=orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Create an order")
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        user = request.user()

        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data , status=status.HTTP_201_CREATE)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    
class OrderDetailView(generics.GenericAPIView):

    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="View the detail of an order by its ID")
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Update an order by its ID")
    def put (self, request, order_id):
        data = request.data
        order = get_object_or_404(Order, pk=order_id)        
        serializer = self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data , status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(operation_summary="Delete an order by its ID")
    def delete (self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateOrderStatusView(generics.GenericAPIView):

    serializer_class = serializers.OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="Update the status of an order")
    def put(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        data = request.data
        serializer = self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data , status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrdersView(generics.GenericAPIView):    

    serializer_class = serializers.OrderDetailSerializer  
    permission_classes=[IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(operation_summary="Get all orders made by a specific user")
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        orders = Order.objects.filter(customer=user)
        serializer = self.serializer_class(instance=orders, many=True)
        return Response(data=serializer.data , status=status.HTTP_200_OK)


class UserOrderDetailView(generics.GenericAPIView):    

    serializer_class = serializers.OrderDetailSerializer   
    permission_classes=[IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(operation_summary="Get the detail of an order made by a specific user")
    def get(self, request, user_id, order_id):
        user = get_object_or_404(User, pk=user_id)
        queryset = Order.objects.filter(pk=order_id, customer=user_id)
        order = get_object_or_404(queryset)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data , status=status.HTTP_200_OK)