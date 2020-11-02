from django import forms

from . import models

class SuggestionForm(forms.Form):
    suggestion = forms.CharField(
        label='What is your favorite color?',
        required=True,
        max_length=240,
        
    )

    def save(self, request):
        suggestion_instance = models.SuggestionModel()
        suggestion_instance.suggestion = self.cleaned_data["suggestion"]
        suggestion_instance.author = request.user
        suggestion_instance.save()
        return suggestion_instance