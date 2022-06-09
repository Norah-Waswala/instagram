from .models import Profile, Post
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['profile','likes','posted_at']
        
class DetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        
class authform(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')