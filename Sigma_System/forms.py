from django import forms


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
    """