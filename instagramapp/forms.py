
  
from .models import Profile, Image
from django import forms

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['profile','likes','Imageed_at']
        
class DetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        
class authform(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')