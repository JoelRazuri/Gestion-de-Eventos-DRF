from django.db import models
from django.contrib.auth.models import AbstractUser

# Options for rol attribute
ROLE_USER_CHOICES = [
    (1, 'Administrador'),
    (2, 'Organizador'),
    (3, 'Usuario'),
]

# Model based on AbstractUser, a class thaht Django includes 
class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, blank=False, null=False, unique=True, verbose_name='Nombre de usuario')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nombres')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Apellidos')
    email = models.EmailField(unique=True, verbose_name='Email')
    password = models.CharField(max_length=100, verbose_name='Contraseña')
    role = models.IntegerField(choices=ROLE_USER_CHOICES, verbose_name='Rol', default=3)


    def __str__(self):
        return self.username  
    

    