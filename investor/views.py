from django.shortcuts import render
from authentication.models import User
#from investment.views import IsSuperUser
from investment.models import Installment, Investors, Investment
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework import generics, status, views, permissions, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from authentication.utils import serial_investor, investor_slug
from .models import Risk, Interest, InvestmentSize, Period, Expectations
from .serializers import UpdateInvestorSerializer, ApproveInvestorInstallmentSerializer, ApproveInstallmentSerializer, CreateInstallmentSerializer, InstallmentSerializer, InvestorExportSerializer, UserInvestorSerializer, AdminUInvestorSerializer, CreateInvestorSerializer, ApproveInvestorSerializer, CloseInvestorSerializer, InvestorSerializer, AdminInvestorSerializer, PeriodSerializer, SizeSerializer, RiskSerializer, InterestSerializer, ExpectationsSerializer
from .permissions import IsOwner, IsUserApproved
from django.db.models import Sum, Aggregate, Avg, Count
from django.http import JsonResponse, Http404, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
import csv
from django.core.mail import send_mail as sender
# Create your views here.


def isApproved(id):
    query = User.objects.filter(id=id).values_list('is_approved', flat=True)[0]
    return query


def getInvesmentAmount(id):
    query = Investment.objects.filter(
        id=id).values_list('amount', flat=True)[0]
    return query


def getInstallmentId(investor):
    query = Installment.objects.filter(
        investor=investor).values_list('id', flat=True)[0]
    if query is None:
        return Response({"error": "Investor not valid"},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        return int(query)


def getInvestorId(id):
    query = Installment.objects.filter(
        id=id).values_list('investor', flat=True)[0]
    if query is None:
        return Response({"error": "Installment not valid"},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        return int(query)


def getInvestorAmount(id):
    query = Investors.objects.filter(
        id=id).values_list('amount', flat=True)[0]
    if query is None:
        return Response({"error": "Investor not valid"},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        return int(query)


def getBidPrice(id):
    query = Investors.objects.filter(
        id=id).values_list('bid_price', flat=True)[0]
    if query is None:
        return Response({"error": "Investor not valid"},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        return int(query)


def getInstallment(id):
    try:
        return Installment.objects.get(id=id)
    except Installment.DoesNotExist:
        raise Http404


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class PeriodListAPIView(ListCreateAPIView):
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()
    permission_classes = (IsAuthenticated, IsSuperUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['period', 'is_verified']
    search_fields = ['period']
    ordering_fields = ['period', 'id', 'is_verified']

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class PeriodAllListAPIView(ListAPIView):
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()
    # permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['period', 'is_verified']
    search_fields = ['period']
    ordering_fields = ['period', 'id', 'is_verified']

    def get_queryset(self):
        return self.queryset.all()


class PeriodDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PeriodSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUser,)
    queryset = Period.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()


class RiskListAPIView(ListCreateAPIView):
    serializer_class = RiskSerializer
    queryset = Risk.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class RiskAllListAPIView(ListAPIView):
    serializer_class = RiskSerializer
    queryset = Risk.objects.all()
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class RiskDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RiskSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUser,)
    queryset = Risk.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()


class InterestListAPIView(ListCreateAPIView):
    serializer_class = InterestSerializer
    queryset = Interest.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class InterestAllListAPIView(ListAPIView):
    serializer_class = InterestSerializer
    queryset = Interest.objects.all()
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()


class InterestDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = InterestSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUser,)
    queryset = Interest.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()


class SizeListAPIView(ListCreateAPIView):
    serializer_class = SizeSerializer
    queryset = InvestmentSize.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class SizeAllListAPIView(ListAPIView):
    serializer_class = SizeSerializer
    queryset = InvestmentSize.objects.all()

    def get_queryset(self):
        return self.queryset.all()


class SizeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SizeSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminUser,)
    queryset = InvestmentSize.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()


class InvestmentAPIView(generics.GenericAPIView):
    serializer_class = CreateInvestorSerializer
    serializer_installment_class = CreateInstallmentSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsUserApproved,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, id):
        try:
            return Investment.objects.get(id=id)
        except Investment.DoesNotExist:
            raise Http404

    def post(self, request, id, format=None):

        if (isApproved(request.user.id) == False):
            return Response({"status": "error",  "error": "User account not approved"},
                            status=status.HTTP_400_BAD_REQUEST)
        investment_id = self.get_object(id)
        serial_invest = str(serial_investor())
        if (int(request.data.get('amount')) < getInvesmentAmount(id)):
            investordata = {
                'amount': request.data.get('amount'),
                'bid_price': request.data.get('bid_price'),
                'volume': request.data.get('volume'),
                'investment_type': request.data.get('investment_type'),
                'slug': str(investor_slug()),
                'investment': id,
                'investor': self.request.user.id,
                'serialkey': serial_invest,
                'is_approved': False,
                'is_closed': False,
            }
            serializer = self.serializer_class(data=investordata)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            investor_data = serializer.data
            installmentdata = {
                'amount': request.data.get('amount'),
                'investor': investor_data['id'],
                'serialkey': serial_invest,
                'is_approved': False,
            }
            serializer_in = self.serializer_installment_class(
                data=installmentdata)
            serializer_in.is_valid(raise_exception=True)
            serializer_in.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error",  "error": "Amount cannot exceed Invesment amount"},
                            status=status.HTTP_400_BAD_REQUEST)


class InstallmentAPIView(generics.GenericAPIView):
    serializer_class = CreateInvestorSerializer
    serializer_installment_class = CreateInstallmentSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsUserApproved,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, id):
        try:
            return Investors.objects.get(id=id)
        except Investment.DoesNotExist:
            raise Http404

    def post(self, request, id, format=None):

        if (isApproved(request.user.id) == False):
            return Response({"status": "error",  "error": "User account not approved"},
                            status=status.HTTP_400_BAD_REQUEST)
        investment_id = self.get_object(id)
        serial_invest = str(serial_investor())
        if (int(request.data.get('amount')) + getInvestorAmount(id) <= getBidPrice(id)):
            installmentdata = {
                'amount': request.data.get('amount'),
                'slug': str(investor_slug()),
                'investor': id,
                'serialkey': serial_invest,
                'is_approved': False,

            }
            serializer_in = self.serializer_installment_class(
                data=installmentdata)
            serializer_in.is_valid(raise_exception=True)
            serializer_in.save()
            return Response(serializer_in.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error",  "error": "Amount cannot exceed Invesment amount"},
                            status=status.HTTP_400_BAD_REQUEST)


class AdminInvestmentAPIView(generics.GenericAPIView):
    serializer_class = CreateInvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, id):
        try:
            return Investment.objects.get(id=id)
        except Investment.DoesNotExist:
            raise Http404

    def get_user_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, id, format=None):

        if (isApproved(request.user.id) == False):
            return Response({"status": "error",  "error": "User account not approved"},
                            status=status.HTTP_400_BAD_REQUEST)
        investment_id = self.get_object(id)
        user_id = self.get_user_object(request.data.get('investor'))
        if (request.data.get('amount') > getInvesmentAmount(id)):

            if int(request.data.get('amount')) > request.data.get('bid_price'):
                return Response({"status": "error",  "error": "Amount cannot be greater than bid price"},
                                status=status.HTTP_400_BAD_REQUEST)
            investordata = {
                'amount': request.data.get('amount'),
                'bid_price': request.data.get('bid_price'),
                'volume': request.data.get('volume'),
                'investment_type': request.data.get('investment_type'),
                'slug': str(investor_slug()),
                'investment': id,
                'investor': request.data.get('investor'),
                'serialkey': str(serial_investor()),
                'is_approved': False,
                'is_closed': False,
            }
            serializer = self.serializer_class(data=investordata)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error",  "error": "Amount cannot exceed Invesment amount"},
                            status=status.HTTP_400_BAD_REQUEST)


class InvestorListAPIView(ListAPIView):
    serializer_class = InvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsUserApproved, )
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['investment__name', 'investment__location']
    search_fields = ['investment__name', 'investment__location']

    def get_queryset(self):
        return self.queryset.filter(investor=self.request.user)


class InvestorDetailAPIView(RetrieveAPIView):
    serializer_class = InvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsUserApproved,)
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(investor=self.request.user)


class TotalAmountAPIView(generics.GenericAPIView):
    serializer_class = InvestorSerializer
    permission_classes = (IsAuthenticated, IsUserApproved,)

    def get(self, format=None):
        item = Investors.objects.filter(
            is_approved=True, investment__currency__name="NGN", investor=self.request.user.id).aggregate(amount=Sum('amount'))
        if item:
            return Response(item, status=status.HTTP_200_OK)
        else:
            return Response({"amount": "0",  "error": "No verified investment"},
                            status=status.HTTP_200_OK)


class TotalAmountClosedAPIView(generics.GenericAPIView):
    serializer_class = InvestorSerializer
    permission_classes = (IsAuthenticated, IsUserApproved,)

    def get(self, format=None):
        item = Investors.objects.filter(
            is_approved=True, is_closed=True, investor=self.request.user.id).aggregate(amount=Sum('amount'))
        if item:
            return Response(item, status=status.HTTP_200_OK)
        else:
            return Response({"amount": "0",  "error": "No verified investment"},
                            status=status.HTTP_200_OK)


class TotalInvestmentsAPIView(generics.GenericAPIView):
    serializer_class = InvestorSerializer
    permission_classes = (IsAuthenticated, IsUserApproved,)

    def get(self, format=None):

        item = Investors.objects.filter(
            is_approved=True).count()
        if item:
            return Response({"investments": item}, status=status.HTTP_200_OK)
        else:
            return Response({"investments": "0",  "error": "No verified investment"},
                            status=status.HTTP_200_OK)


class TotalInvestmentRoomAPIView(generics.GenericAPIView):
    serializer_class = InvestorSerializer
    permission_classes = (IsAuthenticated, IsUserApproved,)

    def get(self, format=None):

        # item = Investors.objects.filter(
        #    is_approved=True).annotate(unique_names=Count('investment', distinct=True))
        item = Investors.objects.filter(is_approved=True).values(
            'investment').distinct().count()
        if item:
            return Response(item, status=status.HTTP_200_OK)
        else:
            return Response({"investments": "0",  "error": "No verified investment"},
                            status=status.HTTP_200_OK)


class AdminInvestorListAPIView(ListAPIView):
    serializer_class = InvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        return self.queryset.all()


class IssuerSingleInvestorListAPIView(ListAPIView):
    serializer_class = InvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404

    def get_queryset(self):
        checkInvestor = self.get_object(self.kwargs['id'])
        if(self.request.user.id == checkInvestor.investment.owner.id):
            return self.queryset.filter(investor=self.kwargs['id'])
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class IssuerInvestorDetailsAPIView(RetrieveAPIView):
    serializer_class = InvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsUserApproved,)
    lookup_field = "id"

    def get_object(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404

    def get_queryset(self):
        checkInvestor = self.get_object(self.kwargs['id'])
        if(self.request.user.id == checkInvestor.investment.owner.id):
            return self.queryset.filter(id=self.kwargs['id'])
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class AdminSingleInvestorListAPIView(ListAPIView):
    serializer_class = InvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        return self.queryset.filter(investor=self.kwargs['id'])


class AdminInstallmentListAPIView(ListAPIView):
    serializer_class = InstallmentSerializer
    queryset = Installment.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        return self.queryset.all()


class InvestorAdminListAPIView(generics.GenericAPIView):
    serializer_class = InvestorSerializer
    queryset = Investors.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404


class ContactIssuerAPIView(generics.GenericAPIView):
    serializer_class = AdminUInvestorSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Investment.objects.get(id=pk)
        except Investment.DoesNotExist:
            raise Http404

    def post(self, request, id, format=None):
        checkInvestment = self.get_object(id)
        if request.data.get('message'):
            '''
            email_body = 'Hi ' + \
                self.request.user.firstname + ' ' + self.request.user.lastname +\
                'with email address ' + self.request.user.email + 'sent the message below' +\
                request.data.get('message')
            data = {'email_body': email_body, 'to_email': checkInvestment.owner.email,
                    'email_subject': 'Project Enquiry'}
            sender(data['email_subject'], data['email_body'],
                   'no-reply@yieldroom.ng', [data['to_email']])'''
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"status": "error",  "error": "Message is empty"},
                            status=status.HTTP_400_BAD_REQUEST)


class AdminUInvestorAPIView(generics.GenericAPIView):
    serializer_class = AdminUInvestorSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def check_investment(self, pk):
        try:
            return Investment.objects.get(id=pk)
        except Investment.DoesNotExist:
            raise Http404

    def get_object(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404

    def check_user(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, id, format=None):
        investment_id = self.get_object(id)
        investor = self.check_user(request.data.get('investor'))
        investment = self.check_investment(request.data.get('investment'))
        investordata = {
            'amount': request.data.get('amount'),
            'bid_price': request.data.get('bid_price'),
            'investor': request.data.get('investor'),
            'investment': request.data.get('investment'),
            'is_approved': request.data.get('is_approved'),
            'approved_by': self.request.user.id,
            'is_closed': request.data.get('is_closed'),
            'closed_by': self.request.user.id,
        }
        serializer = self.serializer_class(investment_id, data=investordata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        snippet = self.get_object(id)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateInvestorAPIView(generics.GenericAPIView):
    serializer_class = UpdateInvestorSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404

    def put(self, request, id, format=None):
        investment_id = self.get_object(id)
        investordata = {
            'amount': request.data.get('amount'),
            'house_number': request.data.get('house_number'),
            'payment': request.data.get('payment'),
        }
        serializer = self.serializer_class(investment_id, data=investordata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        snippet = self.get_object(id)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminApproveInvestorAPIView(generics.GenericAPIView):
    serializer_class = ApproveInvestorSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def check_investor(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404

    def patch(self, request, id, format=None):
        investment_id = self.check_investor(id)
        investordata = {
            'is_approved': request.data.get('is_approved'),
            'approved_by': self.request.user,
        }
        serializer = self.serializer_class(investment_id, data=investordata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCloseInvestorAPIView(generics.GenericAPIView):
    serializer_class = CloseInvestorSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def check_investor(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404

    def patch(self, request, id, format=None):
        investment_id = self.check_investor(id)
        investordata = {
            'is_closed': request.data.get('is_closed'),
            'closed_by': self.request.user,
        }
        serializer = self.serializer_class(investment_id, data=investordata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApproveInvestorAPIView(generics.GenericAPIView):
    serializer_class = ApproveInvestorSerializer
    serializer_installment_class = ApproveInstallmentSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404

    def patch(self, request, id, format=None):
        investment_id = self.get_object(id)
        investordata = {
            'is_approved': request.data.get('is_approved'),
            'approved_by': self.request.user.id,
        }
        serializer = self.serializer_class(investment_id, data=investordata)
        if serializer.is_valid():
            serializer.save()

        installment_id = getInstallmentId(id)
        get_installment_id = getInstallment(installment_id)
        installmentdata = {
            'is_approved': request.data.get('is_approved'),
            'approved_by': self.request.user.id,
        }
        serializer_in = self.serializer_installment_class(
            get_installment_id, data=installmentdata)
        if serializer_in.is_valid():
            serializer_in.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApproveInstallmentAPIView(generics.GenericAPIView):
    serializer_class = ApproveInvestorSerializer
    serializer_add = ApproveInvestorInstallmentSerializer
    serializer_installment_class = ApproveInstallmentSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404

    def patch(self, request, id, format=None):
        #installment_id = getInstallmentId(id)
        investor_id = getInvestorId(id)
        investor_amount = getInvestorAmount(investor_id)
        bid_price = getBidPrice(investor_id)

        # Check if addition of current amount and installment is greater than bid price
        if (investor_amount + int(request.data.get('amount'))) > bid_price:
            return Response({"error": "Total amount cannot be greater than bid price"},
                            status=status.HTTP_400_BAD_REQUEST)

        get_installment_id = getInstallment(id)
        installmentdata = {
            'is_approved': request.data.get('is_approved'),
            'approved_by': self.request.user.id,
        }
        serializer_in = self.serializer_installment_class(
            get_installment_id, data=installmentdata)
        if serializer_in.is_valid():
            serializer_in.save()

        # add installment to current amount
        amount = investor_amount + int(request.data.get('amount'))
        updateInvestorData = {
            'is_approved': True,
            'approved_by': self.request.user.id,
            'amount': amount,
        }

        investment_id = self.get_object(investor_id)
        serializer = self.serializer_add(
            investment_id, data=updateInvestorData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CloseInvestorAPIView(generics.GenericAPIView):
    serializer_class = CloseInvestorSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    def get_object(self, pk):
        try:
            return Investors.objects.get(id=pk)
        except Investors.DoesNotExist:
            raise Http404

    def patch(self, request, id, format=None):
        investment_id = self.get_object(id)
        investordata = {
            'is_closed': request.data.get('is_closed'),
            'closed_by': self.request.user.id,
        }
        serializer = self.serializer_class(investment_id, data=investordata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExportInvestorsCount(generics.GenericAPIView):
    serializer_class = InvestorSerializer
    queryset = Investors.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        writer = csv.writer(response)

        for user in User.objects.all():
            approved_portfolio = Investors.objects.filter(
                investor=user.id)
            #completed_portfolio = approved_portfolio.filter(is_closed=True)

            row = ','.join([
                user.firstname,
                user.lastname
            ])

            writer.writerow(row)

        return response


class AdminUserInvestorListAPIView(ListAPIView):
    serializer_class = UserInvestorSerializer
    queryset = User.objects.all().order_by('-firstname')
    permission_classes = (IsAuthenticated, IsAdminUser,)
    # parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['firstname', 'lastname', 'email', 'phone']
    search_fields = ['firstname', 'lastname', 'email', 'phone']

    def get_queryset(self):
        return self.queryset.all()


class AdminExportInvestorAPIView(generics.GenericAPIView):
    serializer_class = InvestorExportSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=many,
        )

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="investors_export.csv"'

        serializer = self.get_serializer(
            Investors.objects.all(),
            many=True
        )
        header = InvestorExportSerializer.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response
