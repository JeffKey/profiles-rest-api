from django import forms

from . import models

class signUpForm(forms.ModelForm):
    """Allows user to sign up for the event"""

    class Meta:
        model = models.Candidate
        fields = ['user' , 'email']
