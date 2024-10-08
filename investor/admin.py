from django.contrib import admin

# Register your models here.
from .models import InitialInterests, Risk, Interest, InvestmentSize, Period
from investment.models import Installment


class RiskAdmin(admin.ModelAdmin):
    list_display = ['risk', 'is_verified']


admin.site.register(Installment)
admin.site.register(Risk, RiskAdmin)
admin.site.register(Interest)
admin.site.register(InvestmentSize)
admin.site.register(Period)
admin.site.register(InitialInterests)
