from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,
        required=False,
            help_text=_("Optional."),
        label=_("First Name"),)
    last_name = forms.CharField(max_length=30,
        required=False,
            help_text=_("Optional."),
        label=_("Last Name"),)
    email = forms.EmailField(max_length=254,
            help_text=_("Required. Inform a valid email address."),
        label=_("Email"),)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class NameForm(forms.Form):
    name = forms.CharField(label='name to find', max_length=100)
