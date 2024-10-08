from rest_framework import serializers
from .models import SponsorInvestment, Sponsor, Investment, MainRoom, DealType, Currency, InvestmentRoom, Gallery, Investors
from investor.models import Period, Risk
from authentication.models import User
from django.conf import settings
from django.db.models import Sum, Aggregate, Avg
from comment.models import Comment
#from investor.serializers import CommentSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname',
                  'username', 'referral_code', 'phone']


class CommentSerializer(serializers.ModelSerializer):
    responded_by = UserSerializer(many=False, read_only=False)

    class Meta:
        model = Comment
        fields = ['id', 'slug', 'comment',
                  'investor', 'investment', 'is_closed', 'responded_by']

    def get_responsed_by(self, instance):
        return instance.geo_info.responded_by


class UserInvestmentSerializer(serializers.ModelSerializer):
    totalinvestment = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'firstname', 'phone',
                  'lastname', 'email', 'totalinvestment']

    def get_totalinvestment(self, obj):
        return Investment.objects.filter(owner=obj.id).count()
        # return GallerySerializer(logger_queryset, many=True).data


class PeriodInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['id', 'period', ]


class RiskRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = ['id', 'risk', ]


class DealTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DealType
        fields = ['id', 'name', 'is_active', ]


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ['id', 'name', 'is_active', ]


class MainRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainRoom
        fields = ['id', 'slug', 'name', 'description',
                  'is_verified', ]


class SponsorSerializer(serializers.ModelSerializer):
    identity_url = serializers.SerializerMethodField("get_identity_url")

    class Meta:
        model = Sponsor
        fields = ['id', 'nin', 'name', 'dob',
                  'address', 'identity', 'phone', 'is_verified', 'identity_url', ]

    def get_identity_url(self, obj):
        return obj.identity.url


class UpdateSponsorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sponsor
        fields = ['id', 'name', 'dob',
                  'address', 'identity', 'phone', 'is_verified', ]


class ApproveSponsorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sponsor
        fields = ['id', 'is_verified', ]


class SponsorInvestmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = SponsorInvestment
        fields = ['id', 'investment', 'sponsor', ]


class ListSponsorSerializer(serializers.ModelSerializer):
    sponsor = SponsorSerializer(many=False, read_only=False)

    class Meta:
        model = SponsorInvestment
        fields = ['id', 'investment', 'sponsor', ]


class ListInvestorsSerializer(serializers.ModelSerializer):
    investor = UserInvestmentSerializer(many=False, read_only=False)

    class Meta:
        model = Investors
        fields = ['id', 'amount','payment', 'investment', 'investor', ]


class CreateRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentRoom
        fields = ['id', 'main_room', 'slug', 'name', 'description',
                  'is_verified', ]


class RoomSerializer(serializers.ModelSerializer):
    main_room = MainRoomSerializer(many=False, read_only=False)

    class Meta:
        model = InvestmentRoom
        fields = ['id', 'main_room', 'slug', 'name', 'description',
                  'is_verified', ]

    def get_main_room(self, instance):
        return instance.geo_info.main_room


class GallerySerializer(serializers.ModelSerializer):
    gallery_url = serializers.SerializerMethodField("get_image_url")
    # gallery = serializers.ImageField(
    # max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)

    class Meta:
        model = Gallery
        fields = ['id', 'investment', 'gallery', 'gallery_url',
                  'is_featured']

    def get_image_url(self, obj):
        return obj.gallery.url

    '''
    def get_gallery(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.gallery.url)
        '''


class GalleryUDSerializer(serializers.ModelSerializer):
    gallery_url = serializers.SerializerMethodField("get_image_url")
    # gallery = serializers.ImageField(
    # max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)

    class Meta:
        model = Gallery
        fields = ['id', 'gallery',  'is_featured']

    def get_image_url(self, obj):
        return obj.gallery.url

    '''
    def get_gallery(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.gallery.url)
        '''


class GalleryUpdateSerializer(serializers.ModelSerializer):
    # gallery_url = serializers.SerializerMethodField("get_image_url")
    # gallery = serializers.ImageField(
    # max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)

    class Meta:
        model = Gallery
        fields = ['id', 'gallery',  'is_featured']

    '''
    def get_image_url(self, obj):
        return obj.gallery.url


    def get_gallery(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.gallery.url)
        '''


class InvestmentRoomSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    amountAlloted = serializers.SerializerMethodField()
    balanceToBeAlloted = serializers.SerializerMethodField()
    currency = CurrencySerializer(many=False, read_only=False)
    dealtype = DealTypeSerializer(many=False, read_only=False)
    # gallery_set = serializers.StringRelatedField(many=True)
    risk = RiskRoomSerializer(many=False, read_only=False)
    room = RoomSerializer(many=False, read_only=False)
    period = PeriodInvestmentSerializer(read_only=False)
    owner = UserInvestmentSerializer(read_only=False)
    # gallery_investment = GallerySerializer(read_only=False)

    '''
    def get_image(self, gallery):
        pesticide_qs = Gallery.objects.filter(
            gallery__investment=gallery)
        return Gall erySerializer(pesticide_qs, many=True).data
        '''

    class Meta:
        model = Investment
        fields = ['id', 'owner', 'slug', 'name', 'description', 'currency', 'amount',
                  'volume', 'only_returns', 'off_plan', 'outright_purchase', 'outright_purchase_amount', 'project_raise', 'project_cost', 'periodic_payment',
                  'milestone', 'minimum_allotment', 'maximum_allotment', 'offer_price',
                  'amountAlloted', 'balanceToBeAlloted', 'spot_price', 'unit_price', 'dealtype', 'location', 'video', 'room', 'roi', 'period',
                  'annualized',  'risk', 'features', 'is_verified', 'image', 'start_date', 'end_date', 'created_at']

    def get_amountAlloted(self, obj):
        return Investors.objects.filter(investment=obj.id, is_approved=True).aggregate(Sum('amount'))

    def get_balanceToBeAlloted(self, obj):
        totalamount = Investors.objects.filter(
            investment=obj.id, is_approved=True).aggregate(Sum('amount'))
        if obj.project_raise:
            project_raise = int(obj.project_raise)
        else:
            project_raise = 0
        if totalamount.get('amount__sum') is None:
            amount = 0
        else:
            amount = totalamount.get('amount__sum')
        totalBalance = project_raise - amount
        return totalBalance

    def get_image(self, obj):
        logger_queryset = Gallery.objects.filter(investment=obj.id)
        return GallerySerializer(logger_queryset, many=True).data


class InvestmentDetailsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    sponsor = serializers.SerializerMethodField()
    investors = serializers.SerializerMethodField()
    amountAlloted = serializers.SerializerMethodField()
    investorsCount = serializers.SerializerMethodField()
    balanceToBeAlloted = serializers.SerializerMethodField()
    currency = CurrencySerializer(many=False, read_only=False)
    dealtype = DealTypeSerializer(many=False, read_only=False)
    # gallery_set = serializers.StringRelatedField(many=True)
    risk = RiskRoomSerializer(many=False, read_only=False)
    room = RoomSerializer(many=False, read_only=False)
    period = PeriodInvestmentSerializer(read_only=False)
    owner = UserInvestmentSerializer(read_only=False)
    # gallery_investment = GallerySerializer(read_only=False)

    '''
    def get_image(self, gallery):
        pesticide_qs = Gallery.objects.filter(
            gallery__investment=gallery)
        return Gall erySerializer(pesticide_qs, many=True).data
        '''

    class Meta:
        model = Investment
        fields = ['id', 'owner', 'slug', 'name', 'investorsCount', 'description', 'currency', 'amount',
                  'volume', 'only_returns', 'off_plan', 'outright_purchase', 'outright_purchase_amount', 'project_raise', 'project_cost', 'periodic_payment',
                  'milestone', 'minimum_allotment', 'maximum_allotment', 'offer_price', 'title_status', 'construction_status', 'project_status',
                  'amountAlloted', 'balanceToBeAlloted', 'spot_price', 'unit_price', 'dealtype', 'location', 'video', 'room', 'roi', 'period',
                  'annualized',  'risk', 'features', 'is_verified', 'image', 'start_date', 'end_date', 'created_at', 'sponsor', 'investors', ]

    def get_image(self, obj):
        logger_queryset = Gallery.objects.filter(investment=obj.id)
        return GallerySerializer(logger_queryset, many=True).data

    def get_investorsCount(self, obj):
        in_queryset = Investors.objects.filter(investment=obj.id).count()
        return in_queryset

    def get_sponsor(self, obj):
        logger_queryset = SponsorInvestment.objects.filter(investment=obj.id)
        return ListSponsorSerializer(logger_queryset, many=True).data

    def get_investors(self, obj):
        logger_queryset = Investors.objects.filter(investment=obj.id)
        return ListInvestorsSerializer(logger_queryset, many=True).data

    def get_amountAlloted(self, obj):
        return Investors.objects.filter(investment=obj.id, is_approved=True).aggregate(Sum('amount'))

    def get_balanceToBeAlloted(self, obj):
        totalamount = Investors.objects.filter(
            investment=obj.id, is_approved=True).aggregate(Sum('amount'))
        if obj.project_raise:
            project_raise = int(obj.project_raise)
        else:
            project_raise = 0
        if totalamount.get('amount__sum') is None:
            amount = 0
        else:
            amount = totalamount.get('amount__sum')
        totalBalance = project_raise - amount
        return totalBalance

    def get_room(self, instance):
        return instance.geo_info.room

    def get_risk(self, instance):
        return instance.geo_info.risk

    def get_owner(self, instance):
        return instance.geo_info.owner

    def get_userdetails(self, instance):
        return instance.geo_info.userdetails


class InvestmentSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    amountAlloted = serializers.SerializerMethodField()
    balanceToBeAlloted = serializers.SerializerMethodField()
    currency = CurrencySerializer(many=False, read_only=False)
    dealtype = DealTypeSerializer(many=False, read_only=False)
    # gallery_set = serializers.StringRelatedField(many=True)
    risk = RiskRoomSerializer(many=False, read_only=False)
    room = RoomSerializer(many=False, read_only=False)
    period = PeriodInvestmentSerializer(read_only=False)
    owner = UserInvestmentSerializer(read_only=False)
    investorsCount = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    canInvestorComment = serializers.SerializerMethodField()
    canIssuerComment = serializers.SerializerMethodField()

    # gallery_investment = GallerySerializer(read_only=False)

    '''
    def get_image(self, gallery):
        pesticide_qs = Gallery.objects.filter(
            gallery__investment=gallery)
        return GallerySerializer(pesticide_qs, many=True).data
        '''

    class Meta:
        model = Investment
        fields = ['id', 'canInvestorComment', 'canIssuerComment', 'comment', 'owner', 'slug', 'name', 'description', 'currency', 'amount',
                  'volume', 'only_returns', 'off_plan', 'outright_purchase', 'outright_purchase_amount', 'project_raise', 'project_cost', 'periodic_payment', 'milestone', 'minimum_allotment', 'maximum_allotment', 'offer_price',
                  'amountAlloted', 'balanceToBeAlloted', 'spot_price', 'unit_price', 'dealtype', 'location', 'video', 'room', 'roi', 'period',
                  'annualized',  'risk', 'features', 'is_verified', 'is_closed', 'image', 'start_date', 'end_date', 'created_at', 'investorsCount', 'title_status', 'construction_status', 'project_status']

    def get_image(self, obj):
        logger_queryset = Gallery.objects.filter(
            investment=obj.id).order_by('-is_featured')
        return GallerySerializer(logger_queryset, many=True).data

    def get_investorsCount(self, obj):
        in_queryset = Investors.objects.filter(investment=obj.id).count()
        return in_queryset

    def get_comment(self, obj):
        queryset = Comment.objects.filter(investment=obj.id)
        return CommentSerializer(queryset, many=True).data

    def get_canInvestorComment(self, obj):
        user_id = self.context['request'].user.id
        checkExist = Investors.objects.filter(
            investment=obj.id, investor=user_id)
        if checkExist:
            investor_can_comment = True
        else:
            investor_can_comment = False
        return investor_can_comment

    def get_canIssuerComment(self, obj):
        user_id = self.context['request'].user.id
        checkExist = Investment.objects.filter(
            id=obj.id, owner=user_id)
        if checkExist:
            issuer_can_comment = True
        else:
            issuer_can_comment = False
        return issuer_can_comment

    def get_amountAlloted(self, obj):
        return Investors.objects.filter(investment=int(obj.id), is_approved=True).aggregate(Sum('amount'))

    def get_balanceToBeAlloted(self, obj):
        totalamount = Investors.objects.filter(
            investment=int(obj.id), is_approved=True).aggregate(Sum('amount'))

        if obj.project_raise:
            project_raise = int(obj.project_raise)
        else:
            project_raise = 0

        if totalamount.get('amount__sum') is None:

            totalBalance = project_raise - 0
        else:
            totalBalance = project_raise - \
                int(totalamount.get('amount__sum'))

        return totalBalance

    '''
    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image_url)
        '''

    def get_room(self, instance):
        return instance.geo_info.room

    def get_risk(self, instance):
        return instance.geo_info.risk

    def get_owner(self, instance):
        return instance.geo_info.owner

    def get_userdetails(self, instance):
        return instance.geo_info.userdetails


class TotalInvestmentSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField()
    # amount = serializers.SerializerMethodField()

    class Meta:
        model = Investment
        fields = ['amount']

    '''
    def get_amount(self, obj):
        queryset = Investment.objects.aggregate(Sum(obj.amount))
        return queryset'''


class InvestmentOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Investment
        fields = ['id', 'owner', 'slug', 'name', 'description', 'currency', 'amount',
                  'project_cost', 'project_raise', 'periodic_payment', 'milestone', 'minimum_allotment', 'maximum_allotment',
                  'volume', 'only_returns', 'off_plan', 'outright_purchase', 'outright_purchase_amount', 'offer_price', 'spot_price', 'unit_price', 'dealtype', 'location', 'video', 'room', 'roi', 'period',
                  'annualized',  'risk', 'is_closed', 'features', 'is_verified', 'start_date', 'end_date', 'created_at']


class ApproveInvestmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investment
        fields = ['id', 'is_verified']


class CloseInvestmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investment
        fields = ['id', 'is_closed']


class ListSponsorInvestmentSerializer(serializers.ModelSerializer):
    investment = InvestmentSerializer(many=False, read_only=False)

    class Meta:
        model = SponsorInvestment
        fields = ['investment', 'id', 'sponsor', ]


class SponsorListSerializer(serializers.ModelSerializer):
    investmentsCount = serializers.SerializerMethodField()
    identity_url = serializers.SerializerMethodField("get_identity_url")

    class Meta:
        model = Sponsor
        fields = ['id', 'nin', 'name', 'dob',
                  'address', 'identity', 'phone', 'is_verified', 'investmentsCount', 'identity_url', ]

    def get_investmentsCount(self, obj):
        return SponsorInvestment.objects.filter(sponsor=obj.id).count()
        # return GallerySerializer(logger_queryset, many=True).data

    def get_identity_url(self, obj):
        return obj.identity.url


class IssuerOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['id', 'owner', 'slug', 'name', 'description', 'currency',
                  'volume', 'dealtype', 'location', 'video', 'room', 'period', 'title_status', 'construction_status', 'project_status',
                  'risk', 'features', 'start_date', 'end_date', 'created_at']


class IssuerInvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investors
        fields = ['id', 'investor', 'investment_type', 'investment',
                  'serialkey', 'amount', 'volume', 'payment', 'house_number', 'slug']


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
