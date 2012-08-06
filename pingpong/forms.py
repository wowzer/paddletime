from django import forms

from pingpong.models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
