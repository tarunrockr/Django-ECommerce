from django import forms 

class LoginForm(forms.Form):
	email    = forms.EmailField(widget=forms.TextInput(attrs={'class': ["form-control","inp"],'placeholder': 'Enter Email'}))
	password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))