from django.shortcuts import render,redirect,get_object_or_404
from .forms import personform,companyform
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from .models import Company, StockQuotes,Profile,Shares
from django.db import connection
import mysql.connector
from django.contrib.auth.models import User
import datetime
import feedparser
feeds = feedparser.parse('http://feeds.marketwatch.com/marketwatch/realtimeheadlines/')
from django.http import JsonResponse


# Create your views here.

def db(request):
	import requests
	import json
	if request.method=="POST":
		tickera=request.POST['ticker']   #ye query
		mycursor = connection.cursor()
		mycursor.execute("SELECT * FROM stock_quotes where symbol=%s ",[tickera])
		tick = mycursor.fetchall()
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
			print(symbol,dayHigh)
			return render(request,'aa/db.html',{'feeds':feeds,'symbol':symbol,'Open':Open1,'dayHigh':dayHigh,'dayLow':dayLow,'lastPrice':lastPrice,
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
	return render(request,'aa/profile.html',{'feeds':feeds })

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
	return render(request,'aa/dashboard.html',{'feeds':feeds })

def contact(request):
	return render(request,'aa/contact.html')
	
@login_required
def sellbuy(request):
	if request.method == "POST":
		share_choice = request.POST.get('ticker')
		quantity = int(request.POST.get('quantity'))
		share_obj=StockQuotes.objects.get(symbol=share_choice)
		share_price= share_obj.Open
		if quantity>int(0):
			if request.POST.get("button") == "BUY":
				if share_price*quantity <= User.acc_balance:
					trade_obj = TradeShares.objects.create(share=share_choice,choice='Buy',customer=User,bid=share_price,
						volume=quantity,date=datetime.datetime.now())
					trade_obj.save()
					Shares.objects.create(share=share_choice,customer=User,quantity=quantity)
					User.acc_balance=User.acc_balance-(share_price*quantity)		#profile.objects.get(user_ref= request.user)
					return HttpResponse("Share Bought")
			else:
				return HttpResponse("insufficientt BAlance")
			if request.POST.get("button") == "SELL":
				try:
					sell_obj = Shares.objects.get(share=share_choice,customer=User)
					sell_share_quantity = sell_obj.quantity
					if sell_share_quantity>=quantity:
						trade_obj = TradeShares.objects.create(share=share_choice,choice='Sell',customer=User,bid=share_price)
						trade_obj.save()
						t=Shares.objects.get(share=share_choice,customer=User)
						Shares.objects.set(share=share_choice,customer=User,quantity=)
						
						User.total_fund=User.total_fund+(share_price*quantity)
						return HttpResponse("Shares Sold")

					else:
						return HttpResponse("You don't have enough shares !")	
				except Shares.objects:
					return HttpResponse("You have not bought these shares !")		


def something(request,stockQuotes_id):
	post = get_object_or_404(StockQuotes, pk=stockQuotes_id)
	return render(request, 'aa/detail.html',{'post':post,'feeds':feeds})