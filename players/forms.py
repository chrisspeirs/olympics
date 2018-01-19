from django import forms
from .models import Players, Olympics, Game, Tourney, Score

class recordscoreForm(forms.ModelForm):

    message= forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'placeholder': 'score'}), max_length=4000, help_text='enter score')

    class Meta:
        model = Score
        fields=['message']




 
