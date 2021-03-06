from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from django.forms import ModelForm
from .models import MagicNode

class UnameForm(forms.Form):
    uname = forms.SlugField(required = False)

class InterestForm(forms.Form):
    i_like_the_topic = forms.BooleanField(label=_("I like the topic"))
    i_like_the_content = forms.BooleanField(label=_("I like the content"))
    i_am_an_expert = forms.BooleanField(label=_("I am an expert"))


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
    name = forms.CharField(label=_('name to find'), max_length=100)

class AddItemForm(forms.Form):
    name = forms.CharField(label=_('new item name'), max_length=100)
    location = forms.IntegerField(widget=forms.HiddenInput())

class MoveItemForm(forms.Form):
    base_name = forms.CharField(label=_('base item name'), max_length=100)
    location = forms.ChoiceField(choices=((1,'sibling before'),(2,'sibling after'),(3,'first child below')))

class ChangeItemForm(ModelForm):
    class Meta:
        model = MagicNode
        fields = '__all__'

class ChangeTxtForm(ModelForm):
    class Meta:
        model = MagicNode
        fields = [
        'desc', 'text', 'videos','sites',
        'pre_nodes','post_nodes','friends',
        'sib_order', 'video','next',
        'is_ready']

class ChangeFigureForm(ModelForm):
    class Meta:
        model = MagicNode
        fields = ['figure']
