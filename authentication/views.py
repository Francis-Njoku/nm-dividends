from urllib import request
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import status
from investor.models import InitialInterests
from investor.serializers import InitialInterestSerializer
#from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
#from core.auth.serializers import LoginSerializer, RegistrationSerializer
from django.core.mail import send_mail as sender

from rest_framework import filters, generics, status, views, permissions
from .serializers import UserInterestSerializer, SigninSerializer, ReferralSerializer, InviteSerializer, RegisterSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, EmailVerificationSerializer, LoginSerializer, LogoutSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Referrals, User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util, username_generator, referral_generator
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os
import datetime
from django_filters.rest_framework import DjangoFilterBackend

# test


class UserListAPIView(ListAPIView):
    serializer_class = UserInterestSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['firstname', 'lastname',
                        'phone', 'referral_code',
                        ]
    search_fields = ['firstname', 'lastname', 'phone']
    ordering_fields = ['firstname', 'lastname', 'created_at', 'details__interest__interest',
                       'details__risk__risk', 'details__period__period', 'details__investmentsize__investment_size']

    def get_queryset(self):
        return self.queryset.all()


class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserInterestSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()


class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LoginViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = SigninSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class Invite(views.APIView):

    serializer_class = InviteSerializer
    serializer_referral = ReferralSerializer

    invite_param_config = openapi.Parameter(
        'user', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[invite_param_config])
    def get(self, request):
        referral_code = request.GET.get('user')

        item = User.objects.get(referral_code=referral_code)
        # print(item)
        if item.is_approved:
            serializer = InviteSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error",  "error": "Object with referral code does not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
    '''                        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, referral_code):
        if referral_code:
            item = User.objects.filter(
                is_verified=True, referral_code=referral_code)
            if item.exists():
                serializer = InviteSerializer(item)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"res": "Object with referral code does not exists"},
                                status=status.HTTP_400_BAD_REQUEST)
    '''


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    ini_serializer = InitialInterestSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = {
            'firstname': request.data.get('firstname'),
            'lastname': request.data.get('lastname'),
            'username': str(username_generator()),
            'address': request.data.get('address'),
            'linkedln': request.data.get('linkedln'),
            'referral_code': str(referral_generator()),
            'phone': request.data.get('phone'),
            'password': request.data.get('password'),
            'email': request.data.get('email'), }
        #user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        inidata = {'owner': user_data['id'],
                   'risk': request.data.get('risk'),
                   'period': request.data.get('period'),
                   'interest': request.data.get('interest'),
                   'investmentsize': request.data.get('investmentsize'), }
        ini_serial = self.ini_serializer(data=inidata)
        ini_serial.is_valid(raise_exception=True)
        ini_serial.save()
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        print(absurl)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
        sender(data['email_subject'], data['email_body'],
               'ssn@nairametrics.com', [data['to_email']])

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class RegisterReferralView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    referal_serializer = ReferralSerializer
    ini_serializer = InitialInterestSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        if request.data.get('referral_code'):
            check_user = User.objects.get(
                referral_code=request.data.get('referral_code'))
            print(check_user.id)
            if check_user:
                today = datetime.date.today()
                thirty_days_ago = today - datetime.timedelta(days=30)
                check_refers = Referrals.objects.filter(
                    referred=check_user.id, created_at__gte=thirty_days_ago)
                if len(check_refers) > 4:
                    return Response({"status": "error",  "error": "User with referral code exceeded monthly limit"},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = {
                        'firstname': request.data.get('firstname'),
                        'lastname': request.data.get('lastname'),
                        'username': str(username_generator()),
                        'address': request.data.get('address'),
                        'linkedln': request.data.get('linkedln'),
                        'referral_code': str(referral_generator()),
                        'phone': request.data.get('phone'),
                        'password': request.data.get('password'),
                        'email': request.data.get('email'), }
                    #user = request.data
                    serializer = self.serializer_class(data=user)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    user_data = serializer.data
                    refdata = {'owner': user_data['id'],
                               'referred': check_user.id,
                               'status': False, }
                    re_serializer = self.referal_serializer(data=refdata)
                    re_serializer.is_valid(raise_exception=True)
                    re_serializer.save()
                    inidata = {'owner': user_data['id'],
                               'risk': request.data.get('risk'),
                               'period': request.data.get('period'),
                               'interest': request.data.get('interest'),
                               'investmentsize': request.data.get('investmentsize'), }
                    ini_serial = self.ini_serializer(data=inidata)
                    ini_serial.is_valid(raise_exception=True)
                    ini_serial.save()
                    user = User.objects.get(email=user_data['email'])
                    token = RefreshToken.for_user(user).access_token
                    current_site = get_current_site(request).domain
                    relativeLink = reverse('email-verify')
                    absurl = 'http://'+current_site + \
                        relativeLink+"?token="+str(token)
                    print(absurl)
                    email_body = 'Hi '+user.username + \
                        ' Use the link below to verify your email \n' + absurl
                    data = {'email_body': email_body, 'to_email': user.email,
                            'email_subject': 'Verify your email'}

                    Util.send_email(data)
                    return Response(user_data, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error",  "error": "Referral code does not exists"},
                                status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')
        print(email)
        print('trueee')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class LoadUserView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)

            return Response(
                {'user': user.data},
                status=status.HTTP_200_OK
            )

        except:
            return Response(
                {'error': 'Something went wrong when trying to load user'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView2(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(),
        }

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256').decode('utf-8')

        '''response = Response({
            "jwt": token
        }) 
        '''
        response = Response()

        # Send only cookie
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class LoginView3(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(),
        }

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256').decode('utf-8')

        '''response = Response({
            "jwt": token
        }) 
        '''
        response = Response()

        # Send only cookie
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response
