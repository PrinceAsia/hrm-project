from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.conf import settings

from .serializers import (
    ChangePasswordSerializer,
    UpdateAccountSerializer,
    ResetPasswordRequestSerializer,
    ResetPasswordConfirmSerializer,
    UserSerializer
)


@swagger_auto_schema(method='POST', request_body=UserSerializer)
@api_view(['POST'])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


CustomUser = get_user_model()

# Memory-based reset code storage (simple version, use cache or DB in prod)
reset_codes = {}

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    serializer = UpdateAccountSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_account_view(request):
    serializer = UpdateAccountSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='POST', request_body=ChangePasswordSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    serializer = ChangePasswordSerializer(data=request.data)
    user = request.user
    if serializer.is_valid():
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Password changed successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def logout_view(request):
#     request.user.auth_token.delete()
#     return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_request_view(request):
    serializer = ResetPasswordRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=email)
            from random import randint
            code = str(randint(100000, 999999))
            reset_codes[email] = code
            send_mail(
                "Password Reset Code",
                f"Your password reset code is: {code}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            return Response({'detail': 'Reset code sent to email'})
        except CustomUser.DoesNotExist:
            return Response({'email': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_confirm_view(request):
    serializer = ResetPasswordConfirmSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']
        if reset_codes.get(email) == code:
            try:
                user = CustomUser.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                del reset_codes[email]
                return Response({'detail': 'Password reset successfully'})
            except CustomUser.DoesNotExist:
                return Response({'email': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'code': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account_view(request):
    user = request.user
    user.delete()
    return Response({'detail': 'Your account has been deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgwMTUyOTY4LCJpYXQiOjE3NDg2MTY5NjgsImp0aSI6IjUyM2QyYzEyN2EyOTQyMTJhODhjYWUzYjIyNjhkZDQ4IiwidXNlcl9pZCI6MX0.jUNJE3UwIh62cZBMJTm7bxKBDfawPYqfjN9aAnFM6_0