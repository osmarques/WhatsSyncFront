# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pessoa(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    idade = models.IntegerField(verbose_name="Idade do Usuário")
    email = models.EmailField(verbose_name="Endereço de Email")
