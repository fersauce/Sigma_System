from django import forms
from django.contrib.auth.models import User
from Sigma_System.models import Usuario, Proyecto

__author__ = 'sauce'


class RecuperarPassForm(forms.Form):
    """
    Clase que representa el formulario para la recuperacion
    del pass de un usuario.
    """
    correo = forms.EmailField(label='Ingrese su correo')
    """
    Atributo que representa la casilla para cargar el dato del correo
    a enviar el pass.
    """


class AltaProyectoForm(forms.Form):
    """
    Clase que representa al formulario asociado a la creacion de un
    nuevo proyecto
    """
    nombreProyecto = forms.CharField(max_length=30,
                                     widget=forms.TextInput(attrs={
                                         'required': 'true'
                                     }), label='Nombre')
    descripcion = forms.CharField(max_length=150,
                                  widget=forms.Textarea(attrs={
                                      'required': 'true',
                                      'label': 'Descripcion',
                                      'rows': 3, 'cols': 60
                                  }))
    duracion = forms.IntegerField(label='Duracion')

    usuarios = Usuario.objects.all()
    user1 = []
    for usuario in usuarios:
        user1.append((usuario.user, usuario.user.username))
    lider = forms.CharField(max_length=30,
                            widget=forms.Select(
                                choices=user1))


class ModificarProyecto(forms.Form):
    """
    Formulario para la modificacion de un proyecto en particular.
    """
    nombreProyecto = forms.CharField(max_length=30,
                                     widget=forms.TextInput(attrs={
                                         'required': 'true'
                                     }), label='Nombre')
    descripcion = forms.CharField(max_length=150,
                                  widget=forms.Textarea(attrs={
                                      'required': 'true',
                                      'label': 'Descripcion',
                                      'rows': 3, 'cols': 60
                                  }))
    opciones = (('1', 'Pendiente'), ('2', 'Activo'), ('3', 'Finalizado'),
                ('4', 'Cancelado'))
    estado = forms.CharField(max_length=30,
                             widget=forms.Select(choices=opciones))
    costo = forms.IntegerField()


class BusquedaProyectoForm(forms.Form):
    CHOICES = [(1, 'Nombre'), (2, 'Fecha de Inicio'), (3, 'Fecha A Culminar')]

    columna = forms.CharField(max_length=40,
                              widget=forms.Select(choices=CHOICES))
    busqueda = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={}))