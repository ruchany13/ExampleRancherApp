from django import forms

class StudentSearch(forms.Form):
    name = forms.CharField(max_length=200)
    surname = forms.CharField(max_length=200)