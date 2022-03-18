from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from . import serializers


class HelloAuthView(generics.GenericAPIView):

    @swagger_auto_schema(operation_summary="Hello Auth")
    def get(self, request):
        return Response(data={"message":"Hello Auth"}, status=status.HTTP_200_OK)


class UserCreateView(generics.GenericAPIView):
    
    serializer_class  = serializers.UserCreationSerializer

    @swagger_auto_schema(operation_summary="Create a User")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.erros, status_code=status.HTTP_400_BAD_REQUEST)