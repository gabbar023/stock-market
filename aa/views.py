from django.shortcuts import render,redirect
from .forms import personform,companyform
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Company, StockQuotes,Profile
from django.db import connection

import feedparser
feeds = feedparser.parse('http://feeds.marketwatch.com/marketwatch/realtimeheadlines/')
from django.http import JsonResponse


# Create your views here.

def db(request):
	import requests
	import json
	if request.method=="POST":
		tickera=request.POST['ticker']
		mycursor = connection.cursor()
		mycursor.execute("SELECT * FROM stock_quotes where symbol=%s ",[tickera])
		ticka = mycursor.fetchall()
		try:
			tick=json.loads(ticka.content)
		except Exception as e:
			tick="Error...!!!"
		return render(request,'aa/db.html',{'tick':tick})
	else:
		return render(request,'aa/db.html',{'ticker':"Enter a Valid Name"})

def home(request):

	a=StockQuotes.objects.all()
	return render(request,'aa/navbar.html',{'feeds':feeds,'a':a})

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

	

