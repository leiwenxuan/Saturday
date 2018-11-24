from django import forms

class add_form(forms.Form):
    usename = forms.CharField(max_length=20)
    pwd = forms.IntegerField()



