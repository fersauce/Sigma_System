from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django import forms
import datetime
# Create your models here.


class Proyecto(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=200)
    fechaCreacion = models.DateField(default=datetime.datetime.now())
    fechaInicio = models.DateField(default=datetime.datetime.now())
    fechaFinalizacion = models.DateField(
        default=(datetime.datetime.now() + datetime.timedelta(days=1)))
    duracion = models.IntegerField()
    complejidad = models.IntegerField()
    costo = models.IntegerField()
    estado = models.CharField(max_length=15)
    nroFases = models.IntegerField()
    nroMiembros = models.IntegerField()

    def __str__(self):
        return str(self.nombre)


class Fase(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=200)
    posicionFase = models.IntegerField()
    estado = models.CharField(max_length=15)
    fechaInicio = models.DateField(default=datetime.datetime.now())
    fechaFin = models.DateField(
        default=(datetime.datetime.now() + datetime.timedelta(days=1)))


class Permiso(models.Model):
    nombre = models.CharField(max_length=30)
    codigo = models.CharField(max_length=30)


class Rol(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)
    permisos = models.ManyToManyField(Permiso)


class Usuario(models.Model):
    user = models.OneToOneField(User)
    ci = models.CharField(max_length=15, unique=True)
    direccion = models.CharField(max_length=100)
    tel = models.CharField(max_length=20)
    estado = models.BooleanField(default=True)
    roles = models.ManyToManyField(Rol, through='UsuarioRol')

    def __str__(self):
        return self.user.username.__str__()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(user=instance)
    post_save.connect(create_user_profile, sender=User)


class UsuarioRol(models.Model):
    usuario = models.ForeignKey(Usuario)
    rol = models.ForeignKey(Rol)
    idProyecto = models.IntegerField(default=0)
    idFase = models.IntegerField(default=0)
    idItem = models.IntegerField(default=0)


class Atributo(models.Model):
    """
        Clase que define el modelo Atributo
    """
    tipo = models.CharField(max_length=20)
    default = models.CharField(max_length=100, default='')


class TipoDeItem(models.Model):
    """
        Clase que define el modelo TipoDeItem(TI)
    """
    fase = models.ForeignKey(Fase)
    usuario = models.ForeignKey(Usuario)
    nombre = models.CharField(max_length=30)
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.CharField(max_length=100)
    importar = models.BooleanField(default=True)
    atributos = models.ManyToManyField(Atributo, through='AtribTipoDeItem')
    fechaCreacion = models.DateField(default=datetime.datetime.now())


class AtribTipoDeItem(models.Model):
    tipoDeItem = models.ForeignKey(TipoDeItem)
    atributos = models.ForeignKey(Atributo)
    nombre = models.CharField(max_length=30)
    valor = models.CharField(max_length=30)


class Archivo(models.Model):
    archivo_adj = models.FileField(upload_to='archivos')


class LBase(models.Model):
    estado = models.CharField(max_length=15)
    fase = models.ForeignKey(Fase)


class Item(models.Model):
    tipoItems = models.ForeignKey(TipoDeItem)
    version = models.IntegerField(default=1)
    complejidad = models.IntegerField()
    prioridad = models.IntegerField()
    estado = models.CharField(max_length=10, default='Activo')
    items_atrib = models.ManyToManyField(AtribTipoDeItem,
                                         through='ItemAtributosTipoI')
    arch_adjuntos = models.ManyToManyField(Archivo)


class ItemAtributosTipoI(models.Model):
    item = models.ForeignKey(Item)
    tipoItemAtrib = models.ForeignKey(AtribTipoDeItem)
    valor_atrib = models.CharField(max_length=30)


class TipoModificado(models.Model):
    codigo_modificacion = models.CharField(max_length=15)


class Historial(models.Model):
    item = models.ForeignKey(Item)
    nro_version_act = models.IntegerField()
    nro_version_ant = models.IntegerField()
    cod_mod = models.CharField(max_length=15)
    valor_act = models.CharField(max_length=20)
    valor_ant = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=200)
    fecha_mod = models.DateField()


class Solicitud(models.Model):
    justificacion = models.CharField(max_length=500)
    fecha_redaccion = models.DateField()
    nro_votos_posit = models.IntegerField()
    nro_votos_neg = models.IntegerField()
    fecha_respuesta = models.DateField()
    estado = models.CharField(max_length=10, default='Pendiente')
    id_usuario = models.IntegerField()
    item = models.ForeignKey(Item)


class Comite(models.Model):
    obs = models.CharField(max_length=200)
    nro_integ = models.IntegerField()
    fecha_creacion = models.DateField()
    proy = models.ForeignKey(Proyecto)
    usuarios = models.ManyToManyField(Usuario)


class HistorialLineabase(models.Model):
    fecha_cambio = models.DateField()
    id_usuario = models.IntegerField()
    tipo_operacion = models.CharField(max_length=50)
    linea_base = models.ForeignKey(LBase)


class UsuariosXProyecto(models.Model):
    """
    Modelo que representa la conexion entre los usuarios y los proyectos asociados.
    """
    proyecto = models.ForeignKey(Proyecto)
    usuario = models.ForeignKey(Usuario)
