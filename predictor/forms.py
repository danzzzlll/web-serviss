from django import forms

class UserForm(forms.Form):
    comment = forms.TextInput()

class ResultForm(forms.Form):
    result = forms.Textarea()
