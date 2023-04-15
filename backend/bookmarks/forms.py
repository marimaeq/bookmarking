from django import forms

class FolderForm(forms.Form):
    name = forms.CharField()