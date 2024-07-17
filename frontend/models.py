# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.db.models import JSONField


#modelo para los productos
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre

#modelo para el mensaje de los contactos
class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre} - {self.asunto}'

#clase para el manejo de usuarios personalizados y superusuarios
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El nombre de usuario debe ser establecido')
        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

#modelo para los usuarios creados en frontend
class Credenciales(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
# clase para resumen de compra incluyendo unicamente el precio
class Compra(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='compras')
    productos = JSONField()  # Usar JSONField para almacenar productos y sus cantidades
    total = models.DecimalField(max_digits=10, decimal_places=0)
    fecha = models.DateTimeField(auto_now_add=True)
    compra_num = models.IntegerField(default=0)  # Nuevo campo para numeración por usuario

    def save(self, *args, **kwargs):
        if not self.id:  # Solo asignar compra_num si es una nueva compra
            last_compra = Compra.objects.filter(usuario=self.usuario).order_by('-compra_num').first()
            self.compra_num = last_compra.compra_num + 1 if last_compra else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Compra #{self.compra_num} de {self.usuario.username}"

#clase para el detalle de las compras
class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=0)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='detalles_compra')

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en compra {self.compra.id} por {self.usuario.username}"
    