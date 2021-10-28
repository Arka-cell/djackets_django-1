import stripe

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework import status, authentication, permissions
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, OrderItem, PersonalInfos
from .serializers import OrderSerializer, MyOrderSerializer, PersonalInfosSerializer


@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    data = request.data 
    data["user"] = request.user.id
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        paid_amount = sum(
            item.get("quantity") * item.get("product").price
            for item in serializer.validated_data["items"]
        )


        serializer.save(user=request.user, paid_amount=paid_amount)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)


class PersonalInfosView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        if(PersonalInfos.objects.filter(user=user_id).exists()):
            serializer = PersonalInfosSerializer(PersonalInfos.objects.get(user=user_id))
            return Response(status=200, data=serializer.data)
        else:
            new_user_infos = PersonalInfos(
                user=User.objects.get(id=user_id)
            )
            new_user_infos.save()
            serializer = PersonalInfosSerializer(new_user_infos)
            return Response(status=201, data=serializer.data)

    def patch(self, request):
        user_id = request.user.id
        user = PersonalInfos.objects.get(user=user_id)
        serializer = PersonalInfosSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(status=400, data=ValidationError(serializer.errors))
        serializer.is_valid()
        serializer.save()
        return Response(status=200, data=serializer.validated_data)
