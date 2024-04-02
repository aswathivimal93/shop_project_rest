from shop.models import ShopUser,Shop,Consumer
from rest_framework import viewsets,permissions
from .serializers import ShopUserSerializer,ShopSerializer,ConsumerSerializer,PaymentSerializer,UserSerializer
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response



class ShopUserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShopUserSerializer

    def get_queryset(self):
        return ShopUser.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Check if a shop user already exists for the current user
        if ShopUser.objects.filter(user=self.request.user).exists():
            raise PermissionDenied("A shop user already exists for this user.")
        if not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to create Shop.")
        
        # Extract user data from request data
        user_data = self.request.data.pop('user', {})
        
        # Set the user field of the shop user to the current user
        serializer.validated_data['user'] = self.request.user
        
        # Save shop user and user
        shop_user_instance = serializer.save()
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            shop_user_instance.delete()  # Rollback creation if user creation fails
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShopViewSet(viewsets.ModelViewSet):
    permission_classes=[
        permissions.IsAuthenticated
    ]
    serializer_class=ShopSerializer
    def get_queryset(self):
        return Shop.objects.filter(created_by=self.request.user)
    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to create Shop.")
        serializer.save(created_by=self.request.user)
    
   

class ConsumerViewSet(viewsets.ModelViewSet):
    permission_classes=[
       permissions.IsAuthenticated
    ]
    serializer_class=ConsumerSerializer
    def get_queryset(self):
        return Consumer.objects.filter(created_by=self.request.user)
    def perform_create(self, serializer):
        if  self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to create consumer.")
        serializer.save()

class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes=[
       permissions.IsAuthenticated
    ]
    serializer_class=PaymentSerializer
    def get_queryset(self):
        return Consumer.objects.filter(created_by=self.request.user)
    def perform_create(self, serializer):
        ''' if not self.request.user:
            raise PermissionDenied("")'''
        serializer.save()
