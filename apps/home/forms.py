# forms.py

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from .widgets import IconSelect

class PessoaForm(forms.Form):
    mensagem = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 120, 'rows': 1, 'class': 'form-control'}),
        label=''
    )