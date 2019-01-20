from django import forms
from .models import Pack
from colorfield.fields import ColorWidget
from django.contrib.auth.models import User
from users.models import Profile

class PackCreateForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'Enter your pack title'}),
        max_length=100
        )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':'Enter your pack description'}),
        max_length=100
        )
    tags = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':'Enter your tags seperated by comma eg:tag1,tag2'}),
        max_length=99
        )


class LinkCreateForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'Enter your link title'}),
        max_length=50
        )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':'Enter your link description'}),
        max_length=50
        )
    link = forms.URLField(widget=forms.TextInput(attrs={'placeholder':'Enter your link'}))
    link_color = forms.CharField(widget=ColorWidget)
    text_color = forms.CharField(widget=ColorWidget)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['img']