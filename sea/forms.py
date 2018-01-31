from django import forms
from django.forms import ModelForm
from sky.models import MagicNode
from .models import Boat

class AddBoatForm(ModelForm):
    class Meta:
        model = Boat
        #fields = '__all__'
        exclude = ['node']
