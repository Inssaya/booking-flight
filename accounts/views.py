from django.shortcuts import render , redirect
from .models import Profile
# Create your views here.
from .forms import SingUpForm , UserForm, ProfileForm
from django.contrib.auth import authenticate, login

from django.contrib.auth import logout

''' This function checks if the request method is POST (form submitted). If it is, we create a form with
the submitted data. If the form is valid, we save it — this creates a new user in the database. Then we
use authenticate() to make sure the username and password are valid (by checking them against the
database). If they are, it gives us a user object. We then use login(request, user) to log them in
— this attaches the user to the current session. Finally, we redirect the user to the profile page. '''


def signup(request):
    if request.method == 'POST':  #save from 
        form = SingUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user     =authenticate(username=username , password=password)
            login(request, user)
            return redirect('/accounts/profile')
        
    else:   #show from 
        form = SingUpForm()
        
    return render(request, 'registration/signup.html',{'form': form})


def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile/profile.html', {'profile': profile})
   
   
   
   
   
def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
        
    if request.method == 'POST':
       
       User_Form = UserForm(request.POST, instance = request.user)
       Profile_Form = ProfileForm(request.POST , instance  = profile )
       if User_Form.is_valid() and Profile_Form.is_valid():
           User_Form.save()
           myform = Profile_Form.save(commit=False)
           myform.user = request.user
           myform.save()
           return redirect('/accounts/profile')
           
       
       return redirect('/accounts/profile')
        
    
       
    else:
       User_Form = UserForm( instance = request.user)
       Profile_Form = ProfileForm( instance = profile)
    return render(request , 'profile/profile_edit.html',{
        'User_Form': User_Form,
        'Profile_Form': Profile_Form,
        
    })
def logout_view(request):
    logout(request)  
    return redirect('login')