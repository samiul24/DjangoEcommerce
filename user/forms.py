from django import forms
from django.forms import TextInput, EmailInput, Select, FileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from user.models import UserProfile

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=25)
    password = forms.CharField(max_length=25)


class SignUpForm(UserCreationForm):
    username = forms.CharField(required=True, label="",
        widget=forms.TextInput(attrs={'placeholder':'Username'}))

    first_name = forms.CharField(required=True, label="",
        widget=forms.TextInput(attrs={'placeholder':'First name'}))

    last_name = forms.CharField(required=True, label="",
        widget=forms.TextInput(attrs={'placeholder':'Last name'}))

    email = forms.EmailField(required=True, label="",
        widget=forms.TextInput(attrs={'placeholder':'Email'}))

    password1 = forms.CharField(
            required = True,
            label = "",
            widget = forms.PasswordInput(attrs={'placeholder':'Password'})
        )

    password2 = forms.CharField(
            required = True,
            label = "",
            widget = forms.PasswordInput(attrs={'placeholder':'Confirm Password'})
        )
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2',]



class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ( 'username','email','first_name','last_name')
        widgets = {
            'username'  : TextInput(attrs={'class': 'input','placeholder':'Username'}),
            'email'     : EmailInput(attrs={'class': 'input','placeholder':'Email'}),
            'first_name': TextInput(attrs={'class': 'input','placeholder':'First_name'}),
            'last_name' : TextInput(attrs={'class': 'input','placeholder':'Last_name' }),
        }

CITY = [
    ('Dhaka', 'Dhaka'),
    ('Rajshahi', 'Rajshahi'),
    ('Rangpur', 'Rangpur'),
    ]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('Phone', 'Address', 'City','Country','Image',)
        widgets = {
            'Phone'     : TextInput(attrs={'class': 'input','placeholder':'phone'}),
            'Address'   : TextInput(attrs={'class': 'input','placeholder':'address'}),
            'City'      : Select(attrs={'class': 'input','placeholder':'city'},choices=CITY),
            'Country'   : TextInput(attrs={'class': 'input','placeholder':'country' }),
            'Image'     : FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }
