from django.shortcuts import render,redirect,get_object_or_404
from .forms import personform,companyform
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from .models import Company, StockQuotes,Profile,Shares,TradeShares
from django.db import connection
import mysql.connector
from django.contrib.auth.models import User
import datetime
import feedparser
feeds = feedparser.parse('http://feeds.marketwatch.com/marketwatch/realtimeheadlines/')
from django.http import JsonResponse
from django.contrib.auth import get_user_model


# Create your views here.

def db(request):
	import requests
	import json
	if request.method=="POST":
		tickera=request.POST['ticker']   #ye query
		mycursor = connection.cursor()
		mycursor.execute("SELECT * FROM stock_quotes where symbol=%s ",[tickera])
		tick = mycursor.fetchall()
		mycursor.execute("SELECT * FROM company where symbol=%s ",[tickera])
		ctick=mycursor.fetchall()
		if tick:
			tick=list(tick[0])
			symbol=tick[1]
			Open1=tick[2]
			dayHigh=tick[3]
			dayLow=tick[4]
			lastPrice=tick[5]
			previousClose=tick[6]
			change=tick[7]
			pChange=tick[8]
			yearHigh=tick[9]
			yearLow=tick[10]
			chartTodayPath=tick[11]
			ctick=list(ctick[0])
			cname=ctick[1]
			sector=ctick[2]
			revenue=ctick[3]
			market_capital=ctick[4]
			print(symbol,dayHigh)
			return render(request,'aa/db.html',{'feeds':feeds,'cname':cname,'sector':sector,'revenue':revenue,'market_capital':market_capital,'symbol':symbol,'Open':Open1,'dayHigh':dayHigh,'dayLow':dayLow,'lastPrice':lastPrice,
    			'previousClose':previousClose,'change':change,'pChange':pChange,'yearHigh':yearHigh,'yearLow':yearLow,'chartTodayPath':chartTodayPath})
		else:
			return render(request,'aa/db.html',{'ticker':"Enter a Valid Name",'feeds':feeds})
	else:
		return render(request,'aa/db.html',{'ticker':"Enter a Valid Name",'feeds':feeds})

def home(request):
	a=StockQuotes.objects.all()
	return render(request,'aa/navbar.html',{'feeds':feeds,'a':a}) #homepage view

def about(request):
	return render(request,'aa/about.html',{'feeds':feeds })

def nav(request):
	return render(request,'aa/nav.html',{'feeds':feeds})

def register(request):
	if request.user.is_authenticated:
		return redirect('login')
	else:
		if request.method=="POST":
			form=personform(request.POST)
			if form.is_valid():
				form.save()
				username=form.cleaned_data.get('username')
				password=form.cleaned_data.get('password1')
				user=authenticate(username=username,password=password)
				user.profile.fname=form.cleaned_data.get('first_name')
				user.profile.Lname=form.cleaned_data.get('last_name')
				user.profile.email=form.cleaned_data.get('email')			
				messages.success(request, f'Your Account Has Been  Created Successfully  ! Please Login Now')
				login(request,user)
				return redirect('login')
		else:
			form=personform()
			return render(request,'aa/register.html',{'form':form})


def login(request):
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(username=username, password=password)
		if user is not None:
			login(request,user)
			return redirect('home')
		else:
			messages.info(request,f'username or password is Incorrect!')
	context={}
	return render(request,'aa/login.html',context)

@login_required
def profile(request):
	a=request.user
	b=Profile.objects.get(user=a)
	c=Shares.objects.filter(customer=b)
	return render(request,'aa/profile.html',{'feeds':feeds,'b':b,'c':c })


def companyreg(request):
	if request.method=="POST":
		form=companyform(request.POST)
		if form.is_valid():
			company=form.save()
			company.refresh_from_db()
			company.save()
			messages.success(request, f'company registered Successfully!!')
			return redirect('home')
	else:
		form=companyform()
	return render(request,'aa/creg.html',{'form':form})

@login_required
def dashboard(request):
	a=request.user
	b=Profile.objects.get(user=a)
	c=TradeShares.objects.filter(customer=b)
	return render(request,'aa/dashboard.html',{'feeds':feeds, 'b':b,'c':c})

def contact(request):
	return render(request,'aa/contact.html')
	
@login_required
def sellbuy(request):
	if request.method == "POST":
		share_choice = request.POST.get('ticker')
		quantity = int(request.POST.get('quantity')) #idhar tak quantity aur sto
		share_obj=StockQuotes.objects.get(symbol=share_choice)
		share_price= share_obj.Open
		a=request.user
		b=Profile.objects.get(user=a)
		print(a)
		if quantity>int(0):
			if request.POST.get("buy"):
				a=request.user
				
				print(b.acc_balance)
				if share_price*quantity <= b.acc_balance:
					trade_obj = TradeShares.objects.create(share=share_obj,trade_type='Buy',customer=b,bid=share_price,
						volume=quantity,date=datetime.datetime.now())
					trade_obj.save()
					x=Shares.objects.get(share=share_obj,customer=b)
					if x:
						x.quantity+=quantity
						x.save()
					else:
						share_obj=Shares.objects.create(share=share_obj,customer=b,quantity=quantity)
						share_obj.save()
					b.acc_balance=b.acc_balance-(share_price*quantity)
					b.save()
					return HttpResponse("Share Bought")
				else:
					return HttpResponse("insufficientt BAlance")

			if request.POST.get("sell"):
				sell_obj=Shares.objects.get(share=share_obj,customer=b)
				sell_share_quantity=sell_obj.quantity
				if sell_share_quantity>=quantity:
					trade_obj = TradeShares.objects.create(share=share_obj,trade_type='Sell',customer=b,bid=share_price,
						volume=quantity,date=datetime.datetime.now())
					trade_obj.save()
					sell_obj.quantity=sell_obj.quantity-quantity
					sell_obj.save()
					if sell_obj.quantity==0:
						sell_obj.delete()
					b.acc_balance=b.acc_balance+(share_price*quantity)
					b.save()
					return HttpResponse("Shares Sold")
				else:
					return HttpResponse("You don't have enough shares !")	
			else:
				return HttpResponse("You have not bought these shares !")	


def something(request,stockQuotes_id):
	post = get_object_or_404(StockQuotes, pk=stockQuotes_id)
	return render(request, 'aa/detail.html',{'post':post,'feeds':feeds})