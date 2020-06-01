from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    fname=models.CharField(max_length=20, blank=True)
    Lname=models.CharField(max_length=20, blank=True)
    email=models.EmailField(max_length=100)
    acc_balance=models.FloatField(default=500000.00)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()


class StockQuotes(models.Model):
    symbol=models.CharField(unique=True,max_length=20)
    Open=models.FloatField(null=False)
    dayHigh=models.FloatField(null=False)
    dayLow=models.FloatField(null=False)
    lastPrice=models.FloatField(null=False)
    previousClose = models.FloatField(null=False)
    change=models.FloatField(null=False)
    pChange=models.FloatField(null=False)
    yearHigh=models.FloatField(null=False)
    yearLow=models.FloatField(null=False)
    chartTodayPath=models.CharField(max_length=100)
    

    class Meta:
        db_table = 'stock_quotes'

class Company(models.Model):
    symbol = models.CharField(primary_key=True,max_length=20)
    cname = models.CharField(max_length=20)
    sector=models.CharField(max_length=20)
    revenue = models.FloatField(blank=True, null=True)
    market_capital = models.FloatField(blank=True, null=True)
    no_of_stocks=models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.cname+" - "+self.sector

    class Meta:
        db_table = 'company'


class TradeShares(models.Model):
    choice=(('Buy','Buy'),('Sell','Sell'))
    customer=models.ForeignKey(Profile,on_delete=models.CASCADE)
    share=models.ForeignKey(StockQuotes,on_delete=models.CASCADE)
    trade_type = models.CharField(max_length=5,null=True,choices=choice)
    bid = models.FloatField(blank=True, null=True)
    volume=models.IntegerField(blank=True,null=True)
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'trade_shares'

class Shares(models.Model):
    customer=models.ForeignKey(Profile,on_delete=models.CASCADE)
    share=models.ForeignKey(StockQuotes,on_delete=models.CASCADE)
    quantity=models.IntegerField(blank=True,null=False)




           