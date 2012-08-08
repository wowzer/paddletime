from django import forms

from paddletime.models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
