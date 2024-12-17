from django import forms

class FileCreationForm(forms.Form):
    label = forms.CharField()
    
class SaveChangesForm(forms.Form):
    old_label = forms.CharField()
    new_label = forms.CharField(required=False)
    content = forms.CharField(required=False)
