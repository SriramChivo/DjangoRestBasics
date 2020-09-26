from django import forms
from .models import tweet


class TweetForm(forms.ModelForm):
    Dummy = forms.CharField(max_length=60)
    # date_created = forms.CharField(max_length=60,
    #                                widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # updatedTime = forms.CharField(max_length=60,
    #                               widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = tweet
        fields = ["Title", "content", "image",
                  "Dummy"]
