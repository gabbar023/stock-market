ef register(request):
	form_class = personform
	def get(self,request):
		form = self.form_class(None)
		return render(request,'aa/register.html',{'form':form})

	def post(self,request):
		form = self.form_class(request.POST)
		if form.is_valid():
			user= form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user.profile.email = form.cleaned_data['email']
			user.profile.fname = form.cleaned_data['first_name']
			user.profile.Lname=form.cleaned_data['last_name']
			user.set_password(password)
			user.save()
			messages.success(request, f'Your Account Has Been  Created Successfully  ! Please Login Now')
			return redirect('login')
	return render(request,'aa/register.html',{'form':form})