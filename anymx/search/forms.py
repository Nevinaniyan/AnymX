from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)

    # query is the form field that gets the user input


