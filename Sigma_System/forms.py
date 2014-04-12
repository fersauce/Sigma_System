from django import forms

__author__ = 'sauce'


class RecuperarPassForm(forms.Form):
    correo = forms.EmailField(label='Ingrese su correo')