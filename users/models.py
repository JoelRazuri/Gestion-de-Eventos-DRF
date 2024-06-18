from django.db import models
from django.contrib.auth.models import AbstractUser
from .validations import *


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, blank=False, null=False, unique=True, verbose_name='Nombre de usuario')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nombres')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Apellidos')
    email = models.EmailField(unique=True, verbose_name='Email')
    password = models.CharField(max_length=100, verbose_name='Contraseña')
    role = models.IntegerField(validators=[validator_role], verbose_name='Rol')


    def __str__(self):
        return self.username  
    

    