from django import forms

__author__ = 'sauce'


class RecuperarPassForm(forms.Form):
    """
    Clase que representa el formulario para la recuperacion
    del pass de un usuario.
    """
    correo = forms.EmailField(label='Ingrese su correo')
    """
    Atributo que representa la casilla para cargar el dato del correo a enviar el pass.
    """