from django.contrib import admin
from .models import Profile,Company,TradeShares,StockQuotes
from import_export.admin import ImportExportModelAdmin

@admin.register(Profile,Company,StockQuotes,TradeShares)

class ViewAdmin(ImportExportModelAdmin):
	pass