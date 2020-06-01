from django.contrib import admin
from .models import Profile,Company,TradeShares,StockQuotes,Shares
from import_export.admin import ImportExportModelAdmin

@admin.register(Profile,Company,StockQuotes,TradeShares,Shares)

class ViewAdmin(ImportExportModelAdmin):
	pass