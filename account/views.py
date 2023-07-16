from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from account.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserSerializer
from .utils import send_activation_email, send_reset_password_email
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_protect
from django.utils.decorators import method_decorator
from django.conf import settings
# Create your views here.

@method_decorator(ensure_csrf_cookie,name='dispatch')
class GetCSRFToken(APIView):
    permission_classes=[AllowAny]
    def get(self,request):
        return Response({'success':'CSRF cookie set'})

@method_decorator(csrf_protect,name='dispatch')
class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer= UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.create(serializer.validated_data)

            # send account activation email

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse('activate',kwargs={'uid':uid,'token':token})
            activation_url = f'{settings.SITE_DOMAIN} {activation_link}'
            send_activation_email(user.email,activation_url)

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_protect,name='dispatch')
class ActivateView(APIView):
    permission_classes=[AllowAny]


@method_decorator(csrf_protect,name='dispatch')
class ActivationConfirm(APIView):
    permission_classes= [AllowAny]

    def post(self,request):
        uid=request.data.get('uid')
        token=request.data.get('token')
        if not uid or not token:
            return Response({'detail':'Missing uid or token.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uid=force_str(urlsafe_base64_decode(uid))
            user=User.objects.get(pk=uid)
            if default_token_generator.check_token(user,token):
                if user.is_active:
                    return Response({'detail':'Account is already Activated.'},status=status.HTTP_200_OK)
                user.is_active = True
                user.save()
                return Response({'detail':'Account activated successfully.'},status=status.HTTP_200_OK)
            else:
                return Response({'detail':'Invalid activation link'},status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail':'Invalid activation link'},status=status.HTTP_400_BAD_REQUEST)
        
@method_decorator(csrf_protect,name='dispatch')
class LoginView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        email=request.data.get('email')
        password=request.data.get('password')

        user=authenticate(request,email=email,password=password)

        if user is not None:
            if user.is_active:
                login(request,user)
                return Response({'detail':'logged in successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'detail':'Email or password is incorrect.'},status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get(self,request):
        serializer=UserSerializer(request.user)
        data=serializer.data
        data['is_staff']=request.user.is_staff
        return Response(data)  

    def patch(self,request):
        serializer=UserSerializer(request.user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 


class ChangePasswordView(APIView):
    def post(self,request):
        old_password=request.data.get('old_password')
        new_password=request.data.get('new_password')
        user=request.user

        if not user.check_password(old_password):
            return Response({'detail':'Invalid old password'},status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'detail':'Password changed Successfully'},status=status.HTTP_200_OK)
    

class DeleteAccountView(APIView):
    def delete(self,request):
        user=request.user
        user.delete()
        return Response({'detail':'Account deleted successfully'},status=status.HTTP_204_NO_CONTENT)
    
    
    


class LogoutView(APIView):
    def post(self,request):
        logout(request)
        return Response({'detail':'Logged ot successfully.'},status=status.HTTP_200_OK)
    