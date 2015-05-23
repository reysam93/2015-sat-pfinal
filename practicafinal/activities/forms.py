from django import forms
from models import Comment
import models

class ActForm(forms.Form):
    title = forms.CharField(max_length=150, required=False)
    price = forms.IntegerField(required=False)
    date = forms.DateField(required=False)


class RegistryForm(forms.Form):
    nick = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)
    confirmpass = forms.CharField(max_length=50)


class UserPageForm(forms.Form):
    title = forms.CharField(max_length=150, required=False)
    desc = forms.CharField(max_length=300, required=False)
    bgCont = forms.CharField(max_length=30, required=False)
    bgBanner = forms.CharField(max_length=30, required=False)
    bgCopyRigth = forms.CharField(max_length=30, required=False)
    bgLogBox = forms.CharField(max_length=30, required=False)
    bgMenu = forms.CharField(max_length=30, required=False )
    wordColorCont = forms.CharField(max_length=30, required=False)
    wordColorBanner = forms.CharField(max_length=30, required=False)
    wordColorCopyRigth = forms.CharField(max_length=30, required=False)
    wordColorLogBox = forms.CharField(max_length=30, required=False)
    wordColorMenu = forms.CharField(max_length=30, required=False)
    wordSizeCont = forms.IntegerField(required=False)
    wordSizeBanner = forms.IntegerField(required=False)
    wordSizeCopyRigth = forms.IntegerField(required=False)
    wordSizeLogBox = forms.IntegerField(required=False)
    wordSizeMenu = forms.IntegerField(required=False)


class CommentForm(forms.ModelForm):
    #text = models.TextField(default = '')
    class Meta:
        model = Comment
        fields = ['nick', 'text']
