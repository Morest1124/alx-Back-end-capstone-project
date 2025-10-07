from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Serializers import UserSerializer


class RegisterView(APIView):
    """A registration endpoint that accepts username separate from first and last name."""

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import render


