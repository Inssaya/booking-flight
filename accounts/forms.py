from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
#why we import UserCreationForm:
# # 1. It provides a convenient way to create a new user with a username, password, and other fields.

class SingUpForm(UserCreationForm):
   #why we put UserCreationForm as a paremeter:
   # in simple way it is a form for creating a new user account.
    class Meta:
        """
        # Meta class for Django ModelForm

        # The Meta class is an inner class used to provide metadata to the ModelForm.
        # It tells Django which model the form is associated with and which fields to include.

        # 'model = User' links the form to the User model, so form operations (like save) will create or update User instances.
        # This is necessary for Django to know which database table and fields to work with.
        """
        #what is the purpose of this class:
        ## 1. It defines the model that the form is based on (User in this case).
        model = User
        #why we write model = user:
        # 1. It specifies the fields that should be included in the form.
        fields = ('username' , 'email' , 'password1', 'password2')
    
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')
    
        
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'address')        