from django import forms



class AddUrl(forms.Form):
    #url = forms.CharField(label="",max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'http://example.com/'}))
    url = forms.URLField(label="", widget=forms.TextInput(attrs={'placeholder': 'example.com/'}))