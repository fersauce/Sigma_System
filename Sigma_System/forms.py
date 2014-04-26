from django import forms
from django.contrib.auth.models import User
from Sigma_System.models import Usuario, Proyecto


class RecuperarPassForm(forms.Form):
    """
    Clase que representa el formulario para la recuperacion
    del pass de un usuario.
    """
    correo = forms.EmailField(label='Ingrese su correo')
    """
    Atributo que representa la casilla para cargar el dato del correo a enviar el pass.
    """


class FormAltaUsuario(forms.Form):
    """
    Clase que representa el formulario para dar de alta a un usuario.
    """
    nombre_usuario = forms.CharField(max_length=30,
                                     widget=forms.TextInput(attrs={
                                         'placeholder': 'username',
                                         'required': 'True'}))
    """
    Atributo que representa el cuadro de texto para cargar el username
    """
    nombre = forms.CharField(max_length=30,
                                     widget=forms.TextInput(attrs={
                                         'placeholder': 'nombre',
                                         'required': 'True'}))
    """
    Atributo que representa el cuadro de texto para cargar el nombre del usuario
    """
    apellido = forms.CharField(max_length=30,
                                     widget=forms.TextInput(attrs={
                                         'placeholder': 'apellido',
                                         'required': 'True'}))
    """
    Atributo que representa el cuadro de texto para cargar el apellido del usuario
    """
    email = forms.EmailField(widget=forms.TextInput(attrs={
                                         'placeholder': 'e-mail',
                                         'required': 'True'}))
    """
    Atributo que representa el cuadro de texto para cargar el e-mail del usuario
    """
    contrasenha = forms.CharField(max_length=120, widget=forms.PasswordInput(attrs={
                                         'placeholder': 'password',
                                         'required': 'True'}))
    """
    Atributo que representa el cuadro de texto para cargar el password del usuario
    """
    ci = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
                                         'placeholder': 'ci',
                                         'required': 'True'}))
    direccion = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                                         'placeholder': 'direccion',
                                         'required': 'True'}))
    """
    Atributo que representa el cuadro de texto para cargar la direccion del usuario
    """
    tel = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
                                         'placeholder': 'telefono',
                                         'required': 'True'}))
    """
    Atributo que representa el cuadro de texto para cargar el nro. de telefono del usuario
    """


class FormLogin(forms.Form):
    """
    Clase que representa el formulario para loguear a un usuario
    """
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
                                         'placeholder': 'username',
                                         'required': 'True'}))
    """
    Atributo que representa el cuadro de texto para cargar el username
    """
    password = forms.CharField(max_length=120, widget=forms.PasswordInput(attrs={
                                         'placeholder': 'password',
                                         'required': 'True'}))
    """
    Atributo que representa el cuadro de texto para cargar el password del usuario
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


class BusquedaFasesForm(forms.Form):
    CHOICES = [(1, 'Nombre'), (2, 'Estado'), (3, 'Fecha de Inicio'),
               (4, 'Fecha de Culminacion')]
    columna = forms.CharField(max_length=40,
                              widget=forms.Select(choices=CHOICES))
    busqueda = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={}))