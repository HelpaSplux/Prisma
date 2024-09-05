from django import forms

class FileCreationForm(forms.Form):
    label = forms.CharField()