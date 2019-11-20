from django import forms
from .models import Challenge


class ChallengeDetailForm(forms.Form):
    submitted_flag = forms.CharField(label='Flag')


