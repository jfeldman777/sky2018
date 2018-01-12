from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class RenameForm(forms.Form):
    name = forms.CharField(label=_('new name'), max_length=30)
